# Contains the "dummy" rules engine for calculating dynamic values.
# Functions to calculate modifiers, initiative, etc.

import random

def calculate_stats(character):
    """
    Dummy function to calculate dynamic stats based on character data.
    In the future, this will query the DB for base stats, modifiers, active spells, etc.
    """
    # Deterministic "random" stats based on character ID for consistency
    random.seed(character['character_id'])
    
    stats = {
        'Name': character['name'],
        'Level': random.randint(1, 20),
        'HP': random.randint(10, 100),
        'AC': random.randint(10, 25),
        'Strength': random.randint(8, 20),
        'Dexterity': random.randint(8, 20),
        'Constitution': random.randint(8, 20),}
    
    return stats
# Contains the "dummy" rules engine for calculating dynamic values.
# Functions to calculate modifiers, initiative, etc.

from app.models.core import Game, Character
import random
try:
    import app.game_logic.pathfinder1 as pf1
except ImportError:
    pf1 = None

def calculate_stats(character_dict, game_id=None):
    """
    Calculate dynamic stats based on character data and game system.
    """
    stats = {}
    
    # Identify system
    system_name = "Unknown"
    if game_id:
        game = Game.query.get(game_id)
        if game:
            print(f"DEBUG: Game found. ID={game_id}, SystemID={game.system_id}")
            # TODO: Helper to get system name from ID, or just check ID
            # For now, assuming system_id 1 is Pathfinder (based on init_dummy_db)
            if game.system_id == 1: 
                if pf1:
                    print("DEBUG: Dispatching to Pathfinder Logic")
                    return pf1.calculate_stats(character_dict['character_id'])
                else:
                    print("DEBUG: Pathfinder logic not loaded")
                    stats['Error'] = "Pathfinder logic not loaded"
            else:
                 print(f"DEBUG: Unknown System ID {game.system_id}")
        else:
            print(f"DEBUG: Game not found for ID {game_id}")
    else:
        print("DEBUG: No game_id provided to calculate_stats")

    # Fallback / Dummy Logic
    random.seed(character_dict['character_id'])
    
    stats.update({
        'Name': character_dict['name'],
        'System': system_name,
        'Level': random.randint(1, 20),
        'HP': random.randint(10, 100),
        'AC': random.randint(10, 25),
        'Strength': random.randint(8, 20),
        'Dexterity': random.randint(8, 20),
        'Constitution': random.randint(8, 20),
        'Intelligence': random.randint(8, 20),
        'Wisdom': random.randint(8, 20),
        'Charisma': random.randint(8, 20),
        'Active Effects': ['Bless', 'Haste'] if random.random() > 0.5 else ['None']
    })
    
    return stats

def update_character(character_id, form_data, game_id=None):
    """
    Update character data based on game system.
    """
    if game_id:
        game = Game.query.get(game_id)
        if game and game.system_id == 1:
            if pf1:
                return pf1.update_character(character_id, form_data)
            else:
                return False, "Pathfinder logic not loaded"
    
    # Fallback
    return True, "Dummy update (no persistence)"

# In-memory combat state: { game_id: { 'turn': 0, 'participants': [ { 'name': '...', 'initiative': 10, 'effects': [{'name': 'Bless', 'duration': 10}] } ] } }
COMBAT_STATE = {}

def get_combat_state(game_id):
    if game_id not in COMBAT_STATE:
        COMBAT_STATE[game_id] = {'turn': 1, 'participants': []}
    return COMBAT_STATE[game_id]

def add_participant(game_id, name, initiative):
    state = get_combat_state(game_id)
    state['participants'].append({
        'name': name,
        'initiative': initiative,
        'effects': [] # List of {name, duration}
    })
    # Sort by initiative descending
    state['participants'].sort(key=lambda x: x['initiative'], reverse=True)

def next_turn(game_id):
    state = get_combat_state(game_id)
    state['turn'] += 1
    # Decrease duration of effects
    for p in state['participants']:
        new_effects = []
        for e in p['effects']:
            e['duration'] -= 1
            if e['duration'] > 0:
                new_effects.append(e)
        p['effects'] = new_effects

def add_effect(game_id, participant_name, effect_name, duration):
    state = get_combat_state(game_id)
    for p in state['participants']:
        if p['name'] == participant_name:
            p['effects'].append({'name': effect_name, 'duration': duration})
            break