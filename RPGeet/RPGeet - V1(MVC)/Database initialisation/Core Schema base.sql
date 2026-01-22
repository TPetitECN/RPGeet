
CREATE SCHEMA IF NOT EXISTS core
    AUTHORIZATION "RPGeet";

CREATE TABLE IF NOT EXISTS core.users (
                username VARCHAR(64) NOT NULL,
                password VARCHAR(255) NOT NULL,
                CONSTRAINT users_pk PRIMARY KEY (username)
);


CREATE SEQUENCE IF NOT EXISTS core.n_game_system_system_id_seq;

CREATE TABLE IF NOT EXISTS core.n_game_system (
                system_id INTEGER NOT NULL DEFAULT nextval('core.n_game_system_system_id_seq'),
                name VARCHAR(255) NOT NULL,
                CONSTRAINT n_game_system_pk PRIMARY KEY (system_id)
);


ALTER SEQUENCE core.n_game_system_system_id_seq OWNED BY core.n_game_system.system_id;

CREATE SEQUENCE IF NOT EXISTS core.n_sources_source_id_seq;

CREATE TABLE IF NOT EXISTS core.n_sources (
                source_id INTEGER NOT NULL DEFAULT nextval('core.n_sources_source_id_seq'),
                name VARCHAR(255) NOT NULL,
                system_id INTEGER NOT NULL,
                CONSTRAINT n_sources_pk PRIMARY KEY (source_id)
);


ALTER SEQUENCE core.n_sources_source_id_seq OWNED BY core.n_sources.source_id;

CREATE SEQUENCE IF NOT EXISTS core.games_game_id_seq;

CREATE TABLE IF NOT EXISTS core.games (
                game_id INTEGER NOT NULL DEFAULT nextval('core.games_game_id_seq'),
                name VARCHAR(255) NOT NULL,
                system_id INTEGER NOT NULL,
                CONSTRAINT games_pk PRIMARY KEY (game_id)
);


ALTER SEQUENCE core.games_game_id_seq OWNED BY core.games.game_id;

CREATE SEQUENCE IF NOT EXISTS core.r_game_sources_id_game_source_seq;

CREATE TABLE IF NOT EXISTS core.r_game_sources (
                id_game_source INTEGER NOT NULL DEFAULT nextval('core.r_game_sources_id_game_source_seq'),
                game_id INTEGER NOT NULL,
                source_id INTEGER NOT NULL,
                CONSTRAINT r_game_sources_pk PRIMARY KEY (id_game_source)
);


ALTER SEQUENCE core.r_game_sources_id_game_source_seq OWNED BY core.r_game_sources.id_game_source;

CREATE SEQUENCE IF NOT EXISTS core.r_game_user_id_game_user_seq;

CREATE TABLE IF NOT EXISTS core.r_game_user (
                id_game_user INTEGER NOT NULL DEFAULT nextval('core.r_game_user_id_game_user_seq'),
                username VARCHAR(64) NOT NULL,
                game_id INTEGER NOT NULL,
                gamemaster BIT DEFAULT false NOT NULL,
                CONSTRAINT r_game_user_pk PRIMARY KEY (id_game_user)
);


ALTER SEQUENCE core.r_game_user_id_game_user_seq OWNED BY core.r_game_user.id_game_user;

CREATE SEQUENCE IF NOT EXISTS core.characters_character_id_seq;

CREATE TABLE IF NOT EXISTS core.characters (
                character_id INTEGER NOT NULL DEFAULT nextval('core.characters_character_id_seq'),
                id_game_user INTEGER NOT NULL,
                name VARCHAR(255) NOT NULL,
                CONSTRAINT characters_pk PRIMARY KEY (character_id)
);


ALTER SEQUENCE core.characters_character_id_seq OWNED BY core.characters.character_id;

ALTER TABLE core.r_game_user ADD CONSTRAINT users_r_game_user_fk
FOREIGN KEY (username)
REFERENCES core.users (username)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE core.games ADD CONSTRAINT n_game_system_games_fk
FOREIGN KEY (system_id)
REFERENCES core.n_game_system (system_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE core.n_sources ADD CONSTRAINT n_game_system_n_sources_fk
FOREIGN KEY (system_id)
REFERENCES core.n_game_system (system_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE core.r_game_sources ADD CONSTRAINT n_sources_r_game_sources_fk
FOREIGN KEY (source_id)
REFERENCES core.n_sources (source_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE core.r_game_user ADD CONSTRAINT games_r_game_user_fk
FOREIGN KEY (game_id)
REFERENCES core.games (game_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE core.r_game_sources ADD CONSTRAINT games_r_game_sources_fk
FOREIGN KEY (game_id)
REFERENCES core.games (game_id)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;

ALTER TABLE core.characters ADD CONSTRAINT r_game_user_characters_fk
FOREIGN KEY (id_game_user)
REFERENCES core.r_game_user (id_game_user)
ON DELETE NO ACTION
ON UPDATE NO ACTION
NOT DEFERRABLE;