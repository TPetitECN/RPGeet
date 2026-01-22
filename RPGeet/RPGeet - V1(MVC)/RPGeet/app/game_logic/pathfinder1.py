from app.models.pathfinder1 import P1Character, P1Statistics, P1Class, P1Race, P1Skill, P1Source, P1DescriptiveFeatures
from app.models.core import db, Character

def ensure_p1_character_exists(character_id):
    """
    Ensure that a P1Character record exists for the given core character_id.
    If not, create it with default values.
    """
    p1_char = P1Character.query.get(character_id)
    if p1_char:
        return p1_char
    
    # Check if core character exists
    core_char = Character.query.get(character_id)
    if not core_char:
        return None
        
    try:
        # Create minimal defaults
        # 1. Source (Core Rulebook)
        # We assume source 1 exists or similar. 
        # Ideally we should query for "Core Rulebook" or id 1.
        source = P1Source.query.get(1)
        if not source:
            source = P1Source.query.filter_by(name="Core Rulebook").first()
        
        if not source:
             # Try getting ANY source to avoid sequence errors if data exists but not ID 1
             source = P1Source.query.first()
             
        if not source:
             # Create default source if missing
             try:
                 source = P1Source(name="Core Rulebook", core_source_id=1) 
                 db.session.add(source)
                 db.session.flush()
             except Exception:
                 db.session.rollback()
                 # Last ditch: maybe it exists but failed to fetch? Or sequence error.
                 # We can't proceed without source for Race.
                 # But actually Race table has foreign key? Yes.
                 # If flush failed, we are in trouble.
                 # Let's hope query.first() worked.
                 print("Failed to create Source, and none found.")
                 return None

        # 2. Race (Human, Default)
        # Check if a race linked to this source exists
        race = P1Race.query.filter_by(source_id=source.source_id).first()
        if not race:
            # Try any race
            race = P1Race.query.first()
            
        if not race:
            try:
                race = P1Race(source_id=source.source_id)
                db.session.add(race)
                db.session.flush()
            except Exception:
                db.session.rollback()
                print("Failed to create Race.")
                return None
            
        # 3. Features
        features = P1DescriptiveFeatures(
            age=20, gender='', height=175.0, weight=70.0,
            hair_short_desc="", eyes_short_desc="", skin_short_desc=""
        )
        db.session.add(features)
        db.session.flush()
        
        # 4. Statistics
        stats = P1Statistics(
            max_hp=10, lethal_dmg=0, non_lethal_dmg=0,
            base_strength=10, base_dexterity=10, base_constitution=10,
            base_intelligence=10, base_wisdom=10, base_charisma=10
        )
        db.session.add(stats)
        db.session.flush()
        
        # 5. P1Character
        p1_char = P1Character(
            character_id=character_id,
            race_id=race.race_id,
            alignement='N',
            statistics_id=stats.statistics_id,
            name=core_char.name,
            descriptive_features_id=features.descriptive_features_id
        )
        db.session.add(p1_char)
        db.session.commit()
        return p1_char
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating P1 defaults: {e}")
        return None

def calculate_stats(character_id):
    """
    Calculate stats for a Pathfinder 1e character.
    """
    p1_char = ensure_p1_character_exists(character_id)
    if not p1_char:
        return {'Error': 'Pathfinder character data not found could not be created'}
    
    stats = {}
    
    # --- 1. Base Info ---
    stats['name'] = p1_char.name
    stats['player'] = "Unknown" 
    
    race_name = "Unknown"
    if p1_char.race and p1_char.race.source_id:
        from app.models.pathfinder1 import P1Source
        src = P1Source.query.get(p1_char.race.source_id)
        if src: race_name = src.name 
    stats['race'] = race_name
    stats['alignment'] = p1_char.alignement
    
    if p1_char.deities:
        d_rel = p1_char.deities[0]
        stats['deity'] = d_rel.deity.deity_name if d_rel.deity else "None"
    else:
        stats['deity'] = "None"
    
    # --- 2. Attributes & Features ---
    def calc_mod(score): return (score - 10) // 2
    
    st, dx, cn, it, ws, ch = 10, 10, 10, 10, 10, 10
    hp_max, hp_nonlethal = 10, 0
    
    if p1_char.statistics:
        s = p1_char.statistics
        st = s.base_strength or 10
        dx = s.base_dexterity or 10
        cn = s.base_constitution or 10
        it = s.base_intelligence or 10
        ws = s.base_wisdom or 10
        ch = s.base_charisma or 10
        hp_max = s.max_hp
        hp_nonlethal = s.non_lethal_dmg

    stats['attributes'] = [
        {'key': 'str', 'name': 'Strength', 'score': st, 'mod': calc_mod(st)},
        {'key': 'dex', 'name': 'Dexterity', 'score': dx, 'mod': calc_mod(dx)},
        {'key': 'con', 'name': 'Constitution', 'score': cn, 'mod': calc_mod(cn)},
        {'key': 'int', 'name': 'Intelligence', 'score': it, 'mod': calc_mod(it)},
        {'key': 'wis', 'name': 'Wisdom', 'score': ws, 'mod': calc_mod(ws)},
        {'key': 'cha', 'name': 'Charisma', 'score': ch, 'mod': calc_mod(ch)},
    ]
    
    # Store mods for easy access
    mods = {a['key']: a['mod'] for a in stats['attributes']}
    
    if p1_char.descriptive_features:
        f = p1_char.descriptive_features
        stats.update({'age': f.age, 'gender': f.gender, 'height': f.height, 'weight': f.weight, 'eyes': f.eyes_short_desc, 'hair': f.hair_short_desc})
    else:
        stats.update({'age': 0, 'gender': '', 'height': 0, 'weight': 0, 'eyes': '', 'hair': ''})

    stats['hp_total'] = hp_max
    # Assuming lethal_dmg exists on statistics in schema
    current_hp = hp_max - p1_char.statistics.lethal_dmg if p1_char.statistics else hp_max
    stats['hp_current'] = current_hp
    stats['hp_nonlethal'] = hp_nonlethal

    # --- 3. Class Calculation (BAB & Base Saves) ---
    level = 0
    base_bab, base_fort, base_ref, base_will = 0, 0, 0, 0
    class_names = []
    
    for c in p1_char.classes:
        lvl = c.class_level
        level += lvl
        c_name = c.class_.class_name if c.class_ else f"Class {c.class_id}"
        class_names.append(f"{c_name} ({lvl})")
        
        # Stats logic
        if c.class_ and c.class_.class_stats:
            cs = c.class_.class_stats
            
            # BAB: 3=Fast(1), 4=Medium(0.75), 5=Slow(0.5)
            # Note: Math.floor used in PF
            if cs.base_battle_bonus == 3: base_bab += lvl
            elif cs.base_battle_bonus == 4: base_bab += int(lvl * 0.75)
            elif cs.base_battle_bonus == 5: base_bab += int(lvl * 0.5)
            
            # Saves: 1=Good(2 + lvl/2), 2=Poor(lvl/3)
            # Assuming these IDs from previous check
            def get_save(cat_id, level):
                if cat_id == 1: return 2 + int(level / 2)
                return int(level / 3)
                
            base_fort += get_save(cs.fortitude_save_cat, lvl)
            base_ref += get_save(cs.reflex_save_cat, lvl)
            base_will += get_save(cs.will_save_cat, lvl)
            
    stats['class_level'] = f"{', '.join(class_names)}" if level > 0 else "Level 1"
    stats['bab'] = base_bab

    # --- 4. Modifiers Aggregation ---
    # Group modifiers by type to apply stacking rules
    # Types: 2:Armor, 5:Deflection, 6:Dodge, 12:Natural, 15:Resistance, 17:Shield, 18:Size, 20:Untyped
    # Stacking Rule: Max of each type, except Dodge(6) and Untyped(20) and Circumstance(3) stack.
    
    active_mods = p1_char.modifiers # Relationship
    
    def get_bonus_sum(target_types, specific_stat=None):
        """
        Calculate stacked bonus for a list of allowed modifier types.
        TODO: filtering by 'stat' if modifiers have a target column (schema doesn't show one yet?)
        
        """
        relevant_mods = [m for m in active_mods if m.modifier_type_id in target_types]
        
        # Stacking logic
        stacking_types = [3, 6, 20] # Circumstance, Dodge, Untyped
        type_groups = {}
        total = 0
        
        for m in relevant_mods:
            if m.modifier_type_id in stacking_types:
                total += m.value
            else:
                current = type_groups.get(m.modifier_type_id, 0)
                if m.value > current:
                    type_groups[m.modifier_type_id] = m.value
        
        total += sum(type_groups.values())
        return total

    # --- 5. AC Calculation ---
    # AC = 10 + Armor + Shield + Dex + Size + Dodge + Deflection + Natural
    armor_bonus = get_bonus_sum([2]) # Armor
    shield_bonus = get_bonus_sum([17]) # Shield
    nat_armor = get_bonus_sum([12]) # Natural
    deflection = get_bonus_sum([5]) # Deflection
    dodge_bonus = get_bonus_sum([6]) # Dodge
    size_bonus = get_bonus_sum([18]) # Size
    
    # AC Total
    stats['ac_total'] = 10 + armor_bonus + shield_bonus + mods['dex'] + size_bonus + dodge_bonus + deflection + nat_armor
    # Touch: No Armor, Shield, Natural
    stats['ac_touch'] = 10 + mods['dex'] + size_bonus + dodge_bonus + deflection
    # Flat-footed: No Dex, Dodge
    stats['ac_flat'] = 10 + armor_bonus + shield_bonus + size_bonus + deflection + nat_armor
    stats['initiative'] = mods['dex'] # + Improved Init (feat/misc)

    # --- 6. Saves Calculation ---
    # Save = Base + Ability + Resistance + Luck + ...
    # We apply Resistance(15) to all for now as it's the most common (Cloak)
    resistance = get_bonus_sum([15]) 
    
    stats['saves'] = [
        {'key': 'fort', 'name': 'Fortitude', 'total': base_fort + mods['con'] + resistance, 'base': base_fort, 'ability': mods['con'], 'magic': resistance, 'misc': 0},
        {'key': 'ref', 'name': 'Reflex', 'total': base_ref + mods['dex'] + resistance, 'base': base_ref, 'ability': mods['dex'], 'magic': resistance, 'misc': 0},
        {'key': 'will', 'name': 'Will', 'total': base_will + mods['wis'] + resistance, 'base': base_will, 'ability': mods['wis'], 'magic': resistance, 'misc': 0},
    ]

    # --- 7. CMB / CMD ---
    # CMB = BAB + Str + Size
    # CMD = 10 + BAB + Str + Dex + Size + Dodge + Deflection
    stats['cmb'] = base_bab + mods['str'] + size_bonus
    stats['cmd'] = 10 + base_bab + mods['str'] + mods['dex'] + size_bonus + dodge_bonus + deflection

    # --- 8. Skills ---
    stats['skills'] = []
    if p1_char.skills:
        for r_skill in p1_char.skills:
            s_def = r_skill.skill
            s_name = s_def.skill_name.lower()
            
            # Simple Ability Mapping
            abil = 'int'
            if any(x in s_name for x in ['acrobatics', 'stealth', 'ride', 'fly', 'sleight', 'escape']): abil = 'dex'
            elif any(x in s_name for x in ['climb', 'swim']): abil = 'str'
            elif any(x in s_name for x in ['perception', 'sense', 'survival', 'heal']): abil = 'wis'
            elif any(x in s_name for x in ['bluff', 'diplomacy', 'intimidate', 'use magic', 'perform']): abil = 'cha'
            
            ranks = r_skill.base_score
            is_class = r_skill.proficiency
            misc_bonus = 0 # From modifiers?
            
            # Class skill bonus: +3 if ranks > 0 and is_class
            class_bonus = 3 if (is_class and ranks > 0) else 0
            
            total = mods[abil] + ranks + misc_bonus + class_bonus
            
            stats['skills'].append({
                'key': f"skill_{s_def.id_skill}",
                'name': s_def.skill_name,
                'ability': abil,
                'is_class': is_class,
                'ranks': ranks,
                'misc': misc_bonus, # TODO: calculate misc
                'total': total # Not displayed explicitly in template loop inputs but logic useful
            })
            
    if not stats['skills']:
        stats['skills'].append({'key': 'none', 'name': 'No Skills', 'ability': 'int', 'ranks': 0, 'misc': 0})

    stats['weapons'] = [] 
    
    return stats

def update_character(character_id, form_data):
    """
    Update a Pathfinder 1e character from form data.
    """
    # Ensure P1 data exists before updating
    p1_char = ensure_p1_character_exists(character_id)
    
    if not p1_char:
        return False, "Character/P1 Data not found and could not be created"
        
    try:
        # 1. Base Info
        if 'name' in form_data: p1_char.name = form_data['name']
        if 'alignment' in form_data: p1_char.alignement = form_data['alignment']
        
        # 2. Features
        if p1_char.descriptive_features:
            f = p1_char.descriptive_features
            f.age = int(form_data.get('age', f.age) or 0)
            f.gender = form_data.get('gender', f.gender)
            f.height = float(form_data.get('height', f.height) or 0)
            f.weight = float(form_data.get('weight', f.weight) or 0)
            f.eyes_short_desc = form_data.get('eyes', f.eyes_short_desc)
            f.hair_short_desc = form_data.get('hair', f.hair_short_desc)
            
        # 3. Statistics (Attributes & HP)
        if p1_char.statistics:
            s = p1_char.statistics
            s.base_strength = int(form_data.get('str_score', s.base_strength) or 10)
            s.base_dexterity = int(form_data.get('dex_score', s.base_dexterity) or 10)
            s.base_constitution = int(form_data.get('con_score', s.base_constitution) or 10)
            s.base_intelligence = int(form_data.get('int_score', s.base_intelligence) or 10)
            s.base_wisdom = int(form_data.get('wis_score', s.base_wisdom) or 10)
            s.base_charisma = int(form_data.get('cha_score', s.base_charisma) or 10)
            
            s.max_hp = int(form_data.get('hp_total', s.max_hp) or 10)
            s.non_lethal_dmg = int(form_data.get('hp_nonlethal', s.non_lethal_dmg) or 0)
            # Lethal damage might be derived from max - current in some systems, 
            # here we have max and lethal/non-lethal columns. 
            # If form sends 'hp_current', update lethal_dmg = max - current?
            if 'hp_current' in form_data:
                current = int(form_data['hp_current'] or 0)
                s.lethal_dmg = max(0, s.max_hp - current)

        # 4. Skills
        # Iterate over all specific skill inputs in form data
        # Inputs are named skill_{id}_[ranks|misc|class]
        # We need to find valid skill IDs from the form keys
        for key, value in form_data.items():
            if key.startswith('skill_') and '_ranks' in key:
                # Extract ID
                parts = key.split('_') 
                # format: skill_ID_ranks
                if len(parts) == 3 and parts[0] == 'skill' and parts[2] == 'ranks':
                    try:
                        skill_id = int(parts[1])
                        
                        # Find the relationship object
                        # This is inefficient O(N^2) if we iterate, usually better to query directly
                        # But session is open so objects are in identity map
                        
                        # Check if relation exists
                        r_skill = next((r for r in p1_char.skills if r.id_skill == skill_id), None)
                        
                        ranks = int(value or 0)
                        misc = int(form_data.get(f"skill_{skill_id}_misc", 0) or 0)
                        is_class = form_data.get(f"skill_{skill_id}_class") == 'on' 
                        # Checkbox usually sends 'on' if checked, nothing if not. 
                        # But Flask request.form handles boolean check? No, request.form['key'] raises error if missing or returns value.
                        # Wait, form_data from requests usually works this way.
                        
                        if r_skill:
                            r_skill.base_score = ranks # Mapping ranks to base_score as per retrieval
                            r_skill.proficiency = is_class
                            # No misc column in DB yet, ignoring misc
                        else:
                            # Create new relationship?
                            # Need import
                            from app.models.pathfinder1 import P1RSkillCharacter
                            new_r = P1RSkillCharacter(
                                id_skill=skill_id,
                                character_id=character_id,
                                proficiency=is_class,
                                base_score=ranks
                            )
                            db.session.add(new_r)
                            
                    except ValueError:
                        continue

        db.session.commit()
        return True, "Character saved successfully"
        
    except Exception as e:
        db.session.rollback()
        return False, str(e)
