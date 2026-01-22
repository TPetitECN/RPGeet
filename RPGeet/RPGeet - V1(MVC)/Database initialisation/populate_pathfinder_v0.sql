-- Populate Pathfinder Schema

-- 1. Sources
INSERT INTO pathfinder1.sources (source_id, name, core_source_id) VALUES
(1, 'Pathfinder Core Rulebook', 1);

-- 2. Class Stats Categories
-- Assuming these are for: 1=Good, 2=Poor (Saves) and 3=Fast, 4=Medium, 5=Slow (BAB)
-- Need to check if IDs matter, assuming sequential
INSERT INTO pathfinder1.n_class_stats_categories (class_stats_category_id, class_stats_category_name) VALUES
(1, 'Good'),
(2, 'Poor'),
(3, 'Fast'),
(4, 'Medium'),
(5, 'Slow');
-- Reset sequence
SELECT setval('pathfinder1.n_class_stats_categories_class_stats_category_id_seq', (SELECT MAX(class_stats_category_id) FROM pathfinder1.n_class_stats_categories));

-- 3. Class Stats
-- Fighter: Fort Good(1), Ref Poor(2), Will Poor(2), BAB Fast(3)
-- Wizard: Fort Poor(2), Ref Poor(2), Will Good(1), BAB Slow(5)
-- Rogue: Fort Poor(2), Ref Good(1), Will Poor(2), BAB Medium(4)
-- Cleric: Fort Good(1), Ref Poor(2), Will Good(1), BAB Medium(4)
INSERT INTO pathfinder1.class_stats (class_stats_id, Fortitude_save_cat, Reflex_save_cat, Will_save_cat, Base_battle_bonus) VALUES
(1, 1, 2, 2, 3), -- Fighter
(2, 2, 2, 1, 5), -- Wizard
(3, 2, 1, 2, 4), -- Rogue
(4, 1, 2, 1, 4); -- Cleric
SELECT setval('pathfinder1.class_stats_class_stats_id_seq', (SELECT MAX(class_stats_id) FROM pathfinder1.class_stats));

-- 4. Classes
INSERT INTO pathfinder1.classes (class_id, class_name, source_id, class_stats_id) VALUES
(1, 'Fighter', 1, 1),
(2, 'Wizard', 1, 2),
(3, 'Rogue', 1, 3),
(4, 'Cleric', 1, 4);
SELECT setval('pathfinder1.classes_class_id_seq', (SELECT MAX(class_id) FROM pathfinder1.classes));

-- 5. Races
INSERT INTO pathfinder1.races (race_id, source_id) VALUES
(1, 1), -- Human
(2, 1), -- Elf
(3, 1), -- Dwarf
(4, 1); -- Halfling
SELECT setval('pathfinder1.races_race_id_seq', (SELECT MAX(race_id) FROM pathfinder1.races));

-- 6. Deities
INSERT INTO pathfinder1.deities (deity_id, deity_name, deity_alignment, source_id) VALUES
(1, 'Sarenrae', 'NG', 1),
(2, 'Iomedae', 'LG', 1),
(3, 'Desna', 'CG', 1),
(4, 'Asmodeus', 'LE', 1);
SELECT setval('pathfinder1.deities_deity_id_seq', (SELECT MAX(deity_id) FROM pathfinder1.deities));

-- 7. Modifier Types
INSERT INTO pathfinder1.modifier_types (modifier_type_id, modifier_type_name) VALUES
(1, 'Alchemical'), (2, 'Armor'), (3, 'Circumstance'), (4, 'Competence'),
(5, 'Deflection'), (6, 'Dodge'), (7, 'Enhancement'), (8, 'Inherent'),
(9, 'Insight'), (10, 'Luck'), (11, 'Morale'), (12, 'Natural Armor'),
(13, 'Profane'), (14, 'Racial'), (15, 'Resistance'), (16, 'Sacred'),
(17, 'Shield'), (18, 'Size'), (19, 'Trait'), (20, 'Untyped');
SELECT setval('pathfinder1.modifier_types_modifier_type_id_seq', (SELECT MAX(modifier_type_id) FROM pathfinder1.modifier_types));

-- 8. Skills
INSERT INTO pathfinder1.skills (id_skill, skill_name, skill_short_description) VALUES
(1, 'Acrobatics', 'Balance and tumbling'),
(2, 'Appraise', 'Value items'),
(3, 'Bluff', 'Deceive others'),
(4, 'Climb', 'Scale surfaces'),
(5, 'Craft', 'Make items'),
(6, 'Diplomacy', 'Persuade others'),
(7, 'Disable Device', 'Disarm traps'),
(8, 'Disguise', 'Change appearance'),
(9, 'Escape Artist', 'Slip bonds'),
(10, 'Fly', 'Maneuver in air'),
(11, 'Handle Animal', 'Train animals'),
(12, 'Heal', 'Treat wounds'),
(13, 'Intimidate', 'Frighten others'),
(14, 'Knowledge (Arcana)', 'Ancient mysteries'),
(15, 'Knowledge (Dungeoneering)', 'Caverns and oozes'),
(16, 'Linguistics', 'Speak languages'),
(17, 'Perception', 'Notice things'),
(18, 'Perform', 'Entertain'),
(19, 'Profession', 'Job skills'),
(20, 'Ride', 'Control mount'),
(21, 'Sense Motive', 'Detect lies'),
(22, 'Sleight of Hand', 'Pick pockets'),
(23, 'Spellcraft', 'Identify spells'),
(24, 'Stealth', 'Hide and move silently'),
(25, 'Survival', 'Track and forage'),
(26, 'Swim', 'Move in water'),
(27, 'Use Magic Device', 'Activate items');
SELECT setval('pathfinder1.skills_id_skill_seq', (SELECT MAX(id_skill) FROM pathfinder1.skills));

-- 9. Sample Character: Valeros (Human Fighter 1)

-- 9.1 Statistics
INSERT INTO pathfinder1.statistics (statistics_id, max_hp, lethal_dmg, non_lethal_dmg, base_strength, base_dexterity, base_constitution, base_intelligence, base_wisdom, base_charisma) VALUES
(1, 13, 0, 0, 16, 15, 14, 10, 10, 10);
SELECT setval('pathfinder1.statistics_statistics_id_seq', (SELECT MAX(statistics_id) FROM pathfinder1.statistics));

-- 9.2 Descriptive Features
INSERT INTO pathfinder1.descriptive_features (descriptive_features_id, age, gender, height, weight, hair_short_desc, eyes_short_desc, skin_short_desc) VALUES
(1, 25, 'M', 180, 80, 'Brown', 'Brown', 'Tan');
SELECT setval('pathfinder1.descriptive_features_descriptive_features_id_seq', (SELECT MAX(descriptive_features_id) FROM pathfinder1.descriptive_features));

-- 9.3 Character
INSERT INTO pathfinder1.character (character_id, race_id, alignement, statistics_id, name, descriptive_features_id) VALUES
(1, 1, 'NG', 1, 'Valeros', 1);
SELECT setval('pathfinder1.character_character_id_seq', (SELECT MAX(character_id) FROM pathfinder1.character));

-- 9.4 Class Association
INSERT INTO pathfinder1.r_classes_character (id_class_character, class_id, character_id, main_class, class_level) VALUES
(1, 1, 1, true, 1); -- Fighter 1
SELECT setval('pathfinder1.r_classes_character_id_class_character_seq', (SELECT MAX(id_class_character) FROM pathfinder1.r_classes_character));

-- 9.5 Deities
INSERT INTO pathfinder1.r_character_deity (id_character_deity, character_id, deity_id) VALUES
(1, 1, 3); -- Follower of Cayden Cailean (mapped to Desna ID 3 for example as Cayden wasn't added, or just Desna)
-- Actually let's add Cayden Cailean
INSERT INTO pathfinder1.deities (deity_id, deity_name, deity_alignment, source_id) VALUES (5, 'Cayden Cailean', 'CG', 1);
UPDATE pathfinder1.r_character_deity SET deity_id = 5 WHERE id_character_deity = 1;
SELECT setval('pathfinder1.deities_deity_id_seq', (SELECT MAX(deity_id) FROM pathfinder1.deities));
SELECT setval('pathfinder1.r_character_deity_id_character_deity_seq', (SELECT MAX(id_character_deity) FROM pathfinder1.r_character_deity));


-- 9.6 Skills Association (Sample)
-- Valeros skills: Climb, Intimidate, Ride, Swim
INSERT INTO pathfinder1.r_skill_character (id_skill, character_id, proficiency, base_score) VALUES
(4, 1, true, 1), -- Climb (1 rank)
(13, 1, true, 1), -- Intimidate
(20, 1, true, 1), -- Ride
(26, 1, true, 1); -- Swim
