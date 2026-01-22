-- 363 lines
CREATE SCHEMA IF NOT EXISTS pathfinder1
    AUTHORIZATION "RPGeet";

CREATE SEQUENCE pathfinder1.n_sources_source_id_seq;

CREATE TABLE pathfinder1.N_Sources (
                source_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.n_sources_source_id_seq'),
                name VARCHAR NOT NULL,
                core_source_id INTEGER NOT NULL,
                CONSTRAINT n_sources_pk PRIMARY KEY (source_id)

);

ALTER SEQUENCE pathfinder1.n_sources_source_id_seq OWNED BY pathfinder1.N_Sources.source_id;

CREATE SEQUENCE pathfinder1.n_class_stats_categories_class_stats_category_id_seq;

CREATE TABLE pathfinder1.n_class_stats_categories (
                class_stats_category_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.n_class_stats_categories_class_stats_category_id_seq'),
                class_stats_category_name VARCHAR(15) NOT NULL,
                CONSTRAINT n_class_stats_categories_pk PRIMARY KEY (class_stats_category_id)
);


ALTER SEQUENCE pathfinder1.n_class_stats_categories_class_stats_category_id_seq OWNED BY pathfinder1.n_class_stats_categories.class_stats_category_id;

CREATE SEQUENCE pathfinder1.class_stats_class_stats_id_seq;

CREATE TABLE pathfinder1.class_stats (
                class_stats_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.class_stats_class_stats_id_seq'),
                Fortitude_save_cat INTEGER NOT NULL,
                Reflex_save_cat INTEGER NOT NULL,
                Will_save_cat INTEGER NOT NULL,
                Base_battle_bonus INTEGER NOT NULL,
                CONSTRAINT class_stats_pk PRIMARY KEY (class_stats_id)
);


ALTER SEQUENCE pathfinder1.class_stats_class_stats_id_seq OWNED BY pathfinder1.class_stats.class_stats_id;

CREATE SEQUENCE pathfinder1.modifier_types_modifier_type_id_seq;

CREATE TABLE pathfinder1.modifier_types (
                modifier_type_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.modifier_types_modifier_type_id_seq'),
                modifier_type_name VARCHAR(31) NOT NULL,
                CONSTRAINT modifier_types_pk PRIMARY KEY (modifier_type_id)
);


ALTER SEQUENCE pathfinder1.modifier_types_modifier_type_id_seq OWNED BY pathfinder1.modifier_types.modifier_type_id;

CREATE SEQUENCE pathfinder1.skills_id_skill_seq;

CREATE TABLE pathfinder1.skills (
                id_skill INTEGER NOT NULL DEFAULT nextval('pathfinder1.skills_id_skill_seq'),
                skill_name VARCHAR(31) NOT NULL,
                skill_short_description VARCHAR(255) NOT NULL,
                CONSTRAINT skills_pk PRIMARY KEY (id_skill)
);


ALTER SEQUENCE pathfinder1.skills_id_skill_seq OWNED BY pathfinder1.skills.id_skill;

CREATE SEQUENCE pathfinder1.descriptive_features_descriptive_features_id_seq;

CREATE TABLE pathfinder1.descriptive_features (
                descriptive_features_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.descriptive_features_descriptive_features_id_seq'),
                age INTEGER NOT NULL,
                gender VARCHAR(1) NOT NULL,
                height REAL NOT NULL,
                weight REAL NOT NULL,
                hair_short_desc VARCHAR(31) NOT NULL,
                eyes_short_desc VARCHAR(31) NOT NULL,
                skin_short_desc VARCHAR(31) NOT NULL,
                CONSTRAINT descriptive_features_pk PRIMARY KEY (descriptive_features_id)
);


ALTER SEQUENCE pathfinder1.descriptive_features_descriptive_features_id_seq OWNED BY pathfinder1.descriptive_features.descriptive_features_id;

CREATE SEQUENCE pathfinder1.statistics_statistics_id_seq;

CREATE TABLE pathfinder1.statistics (
                statistics_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.statistics_statistics_id_seq'),
                max_hp INTEGER NOT NULL,
                lethal_dmg INTEGER NOT NULL,
                non_lethal_dmg INTEGER NOT NULL,
                base_strength INTEGER,
                base_dexterity INTEGER,
                base_constitution INTEGER,
                base_intelligence INTEGER,
                base_wisdom INTEGER,
                base_charisma INTEGER,
                CONSTRAINT statistics_pk PRIMARY KEY (statistics_id)
);


ALTER SEQUENCE pathfinder1.statistics_statistics_id_seq OWNED BY pathfinder1.statistics.statistics_id;

CREATE SEQUENCE pathfinder1.sources_source_id_seq;

CREATE TABLE pathfinder1.sources (
                source_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.sources_source_id_seq'),
                name VARCHAR(1024) NOT NULL,
                core_source_id INTEGER NOT NULL,
                CONSTRAINT sources_pk PRIMARY KEY (source_id)
);


ALTER SEQUENCE pathfinder1.sources_source_id_seq OWNED BY pathfinder1.sources.source_id;

CREATE SEQUENCE pathfinder1.deities_deity_id_seq;

CREATE TABLE pathfinder1.deities (
                deity_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.deities_deity_id_seq'),
                deity_name VARCHAR NOT NULL,
                deity_alignment VARCHAR(2) NOT NULL,
                source_id INTEGER NOT NULL,
                CONSTRAINT deities_pk PRIMARY KEY (deity_id)
);


ALTER SEQUENCE pathfinder1.deities_deity_id_seq OWNED BY pathfinder1.deities.deity_id;

CREATE SEQUENCE pathfinder1.races_race_id_seq;

CREATE TABLE pathfinder1.races (
                race_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.races_race_id_seq'),
                source_id INTEGER NOT NULL,
                CONSTRAINT races_pk PRIMARY KEY (race_id)
);


ALTER SEQUENCE pathfinder1.races_race_id_seq OWNED BY pathfinder1.races.race_id;

CREATE SEQUENCE pathfinder1.character_character_id_seq;

CREATE TABLE pathfinder1.character (
                character_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.character_character_id_seq'),
                race_id INTEGER NOT NULL,
                alignement VARCHAR(2) DEFAULT 'N' NOT NULL,
                statistics_id INTEGER NOT NULL,
                name VARCHAR(255) NOT NULL,
                descriptive_features_id INTEGER NOT NULL,
                CONSTRAINT character_pk PRIMARY KEY (character_id)
);


ALTER SEQUENCE pathfinder1.character_character_id_seq OWNED BY pathfinder1.character.character_id;

CREATE SEQUENCE pathfinder1.modifiers_id_modifier_seq;

CREATE TABLE pathfinder1.modifiers (
                id_modifier INTEGER NOT NULL DEFAULT nextval('pathfinder1.modifiers_id_modifier_seq'),
                character_id INTEGER NOT NULL,
                modifier_type_id INTEGER NOT NULL,
                value INTEGER DEFAULT 0 NOT NULL,
                duration INTEGER DEFAULT 0,
                CONSTRAINT modifiers_pk PRIMARY KEY (id_modifier)
);


ALTER SEQUENCE pathfinder1.modifiers_id_modifier_seq OWNED BY pathfinder1.modifiers.id_modifier;

CREATE SEQUENCE pathfinder1.r_modifier_origin_modifier_origin_id_seq;

CREATE TABLE pathfinder1.r_modifier_origin (
                modifier_origin_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.r_modifier_origin_modifier_origin_id_seq'),
                id_modifier INTEGER NOT NULL,
                CONSTRAINT r_modifier_origin_pk PRIMARY KEY (modifier_origin_id)
);


ALTER SEQUENCE pathfinder1.r_modifier_origin_modifier_origin_id_seq OWNED BY pathfinder1.r_modifier_origin.modifier_origin_id;

CREATE TABLE pathfinder1.r_skill_character (
                id_skill INTEGER NOT NULL,
                character_id INTEGER NOT NULL,
                proficiency BOOLEAN DEFAULT false NOT NULL,
                base_score INTEGER DEFAULT 0 NOT NULL,
                CONSTRAINT r_skill_character_pk PRIMARY KEY (id_skill, character_id)
);


CREATE SEQUENCE pathfinder1.r_character_deity_id_character_deity_seq;

CREATE TABLE pathfinder1.r_character_deity (
                id_character_deity INTEGER NOT NULL DEFAULT nextval('pathfinder1.r_character_deity_id_character_deity_seq'),
                character_id INTEGER NOT NULL,
                deity_id INTEGER NOT NULL,
                CONSTRAINT r_character_deity_pk PRIMARY KEY (id_character_deity)
);


ALTER SEQUENCE pathfinder1.r_character_deity_id_character_deity_seq OWNED BY pathfinder1.r_character_deity.id_character_deity;

CREATE SEQUENCE pathfinder1.classes_class_id_seq;

CREATE TABLE pathfinder1.classes (
                class_id INTEGER NOT NULL DEFAULT nextval('pathfinder1.classes_class_id_seq'),
                class_name VARCHAR(255) NOT NULL,
                source_id INTEGER NOT NULL,
                class_stats_id INTEGER NOT NULL,
                CONSTRAINT classes_pk PRIMARY KEY (class_id)
);


ALTER SEQUENCE pathfinder1.classes_class_id_seq OWNED BY pathfinder1.classes.class_id;

CREATE SEQUENCE pathfinder1.r_classes_character_id_class_character_seq;

CREATE TABLE pathfinder1.r_classes_character (
                id_class_character INTEGER NOT NULL DEFAULT nextval('pathfinder1.r_classes_character_id_class_character_seq'),
                class_id INTEGER NOT NULL,
                character_id INTEGER NOT NULL,
                main_class BOOLEAN NOT NULL,
                class_level INTEGER DEFAULT 1 NOT NULL,
                CONSTRAINT r_classes_character_pk PRIMARY KEY (id_class_character)
);


ALTER SEQUENCE pathfinder1.r_classes_character_id_class_character_seq OWNED BY pathfinder1.r_classes_character.id_class_character;

ALTER TABLE pathfinder1.class_stats ADD CONSTRAINT n_class_stats_categories_class_stats_fk
FOREIGN KEY (Fortitude_save_cat)
REFERENCES pathfinder1.n_class_stats_categories (class_stats_category_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.class_stats ADD CONSTRAINT n_class_stats_categories_class_stats_fk1
FOREIGN KEY (Reflex_save_cat)
REFERENCES pathfinder1.n_class_stats_categories (class_stats_category_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.class_stats ADD CONSTRAINT n_class_stats_categories_class_stats_fk2
FOREIGN KEY (Will_save_cat)
REFERENCES pathfinder1.n_class_stats_categories (class_stats_category_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.class_stats ADD CONSTRAINT n_class_stats_categories_class_stats_fk3
FOREIGN KEY (Base_battle_bonus)
REFERENCES pathfinder1.n_class_stats_categories (class_stats_category_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.classes ADD CONSTRAINT class_stats_classes_fk
FOREIGN KEY (class_stats_id)
REFERENCES pathfinder1.class_stats (class_stats_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.modifiers ADD CONSTRAINT modifier_types_modifiers_fk
FOREIGN KEY (modifier_type_id)
REFERENCES pathfinder1.modifier_types (modifier_type_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.r_skill_character ADD CONSTRAINT skills_r_skill_character_fk
FOREIGN KEY (id_skill)
REFERENCES pathfinder1.skills (id_skill)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.character ADD CONSTRAINT descriptive_features_character_fk
FOREIGN KEY (descriptive_features_id)
REFERENCES pathfinder1.descriptive_features (descriptive_features_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.character ADD CONSTRAINT statistics_character_fk
FOREIGN KEY (statistics_id)
REFERENCES pathfinder1.statistics (statistics_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.classes ADD CONSTRAINT sources_classes_fk
FOREIGN KEY (source_id)
REFERENCES pathfinder1.sources (source_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.races ADD CONSTRAINT sources_races_fk
FOREIGN KEY (source_id)
REFERENCES pathfinder1.sources (source_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.deities ADD CONSTRAINT sources_deities_fk
FOREIGN KEY (source_id)
REFERENCES pathfinder1.sources (source_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.r_character_deity ADD CONSTRAINT deities_r_character_deity_fk
FOREIGN KEY (deity_id)
REFERENCES pathfinder1.deities (deity_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.character ADD CONSTRAINT races_character_fk
FOREIGN KEY (race_id)
REFERENCES pathfinder1.races (race_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.r_classes_character ADD CONSTRAINT character_r_classes_character_fk
FOREIGN KEY (character_id)
REFERENCES pathfinder1.character (character_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.r_character_deity ADD CONSTRAINT character_r_character_deity_fk
FOREIGN KEY (character_id)
REFERENCES pathfinder1.character (character_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.r_skill_character ADD CONSTRAINT character_r_skill_character_fk
FOREIGN KEY (character_id)
REFERENCES pathfinder1.character (character_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.modifiers ADD CONSTRAINT character_modifiers_fk
FOREIGN KEY (character_id)
REFERENCES pathfinder1.character (character_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.r_modifier_origin ADD CONSTRAINT modifiers_r_modifier_origin_fk
FOREIGN KEY (id_modifier)
REFERENCES pathfinder1.modifiers (id_modifier)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE pathfinder1.r_classes_character ADD CONSTRAINT classes_r_classes_character_fk
FOREIGN KEY (class_id)
REFERENCES pathfinder1.classes (class_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;