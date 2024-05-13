-- from the terminal run:
-- psql < test_seed.sql

DROP DATABASE IF EXISTS test_axe;
CREATE DATABASE test_axe;
\c test_axe

CREATE TABLE judges (
    judge_id SERIAL PRIMARY KEY,
    judge_name TEXT UNIQUE NOT NULL,
    pass_hash TEXT NOT NULL
);

INSERT INTO judges (judge_name, pass_hash)
    VALUES ('judge1', 'scrypt:32768:8:1$M9YNLe14KZgLCnsA$76a151eeb6e6adc8421e4e0f31440be8ac0414ee26e9804f4124cbf3060431b3af4fc4cc03af1fc4b22f48210ec2bed89b5577106ab8137f68fe74717ba660c1');

CREATE TABLE competitors (
    competitor_id SERIAL PRIMARY KEY,
    competitor_first_name TEXT NOT NULL,
    competitor_last_name TEXT NOT NULL
);

INSERT INTO competitors (competitor_first_name, competitor_last_name)
    VALUES ('ann', 'applewood'),
            ('bob', 'berrymore'),
            ('carrie', 'castleman');

CREATE TABLE seasons (
    season_id SERIAL PRIMARY KEY,
    season TEXT NOT NULL,
    start_date DATE NOT NULL
);

INSERT INTO seasons (season, start_date)
    VALUES ('I', '2024-01-20'),
            ('II', '2024-08-15');

CREATE TABLE quarters (
    quarter_id SERIAL PRIMARY KEY,
    season_id INTEGER NOT NULL REFERENCES seasons,
    month INTEGER NOT NULL,
    start_date DATE NOT NULL
);

INSERT INTO quarters (month, season_id, start_date)
    VALUES (1, 1, '2024-01-20'),
            (2, 1, '2024-08-15');

CREATE TABLE laps (
    lap_id SERIAL PRIMARY KEY,
    quarter_id INTEGER NOT NULL REFERENCES quarters,
    counter INTEGER NOT NULL,
    discipline TEXT NOT NULL,
    start_date DATE NOT NULL
);

INSERT INTO laps (quarter_id, counter, discipline, start_date)
    VALUES (1, 1, 'hatchet', '2024-01-20'),
            (2, 1, 'knives', '2024-08-15');

CREATE TABLE tournaments (
    tournament_id SERIAL PRIMARY KEY,
    tournament_name TEXT NOT NULL,
    discipline TEXT NOT NULL,
    tournament_date DATE NOT NULL,
    enrollment_open BOOLEAN DEFAULT TRUE,
    current_round INTEGER,
    double_elemination BOOLEAN DEFAULT FALSE
);

INSERT INTO tournaments (tournament_name, discipline, tournament_date)
    VALUES ('Hatchet Fight', 'Hatchet', '2024-01-20'),
            ('Knife Fight', 'Knives', '2024-06-26');

CREATE TABLE rounds (
    round_id SERIAL PRIMARY KEY,
    bye_competitors INTEGER[],
    matches INTEGER[],
    tournament_id INTEGER NOT NULL REFERENCES tournaments,
    which_round CHAR(1)
);

INSERT INTO rounds (bye_competitors, matches, tournament_id, which_round)
    VALUES ('{0, 0, 0, 0}', '{100, 101, 102, 103}', 1, 'C'),
            ('{0}', '{104}', 1, 'A');

CREATE TABLE enrollment (
    tournament_id INTEGER REFERENCES tournaments,
    season_id INTEGER REFERENCES seasons,
    competitor_id INTEGER NOT NULL REFERENCES competitors
);

INSERT INTO enrollment (season_id, competitor_id)
    VALUES (1, 1),
            (2, 2);

CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    player_1_id INTEGER NOT NULL REFERENCES competitors,
    player_2_id INTEGER NOT NULL REFERENCES competitors,
    winner_id INTEGER REFERENCES competitors,
    tournament_id INTEGER REFERENCES tournaments,
    lap_id INTEGER REFERENCES laps,
    discipline TEXT,
    judge_id INTEGER REFERENCES judges,
    dt TIMESTAMP,
    player_1_total INTEGER,
    player_2_total INTEGER
);

INSERT INTO matches (player_1_id, player_2_id, tournament_id)
    VALUES (1, 2, 1),
            (1, 3, 1);

CREATE TABLE scores (
    score_id SERIAL PRIMARY KEY,
    competitor_id INTEGER NOT NULL REFERENCES competitors,
    match_id INTEGER NOT NULL REFERENCES matches,
    quick_points INTEGER,
    sequence TEXT,
    throw1 INTEGER NOT NULL,
    throw2 INTEGER NOT NULL,
    throw3 INTEGER NOT NULL,
    throw4 INTEGER NOT NULL,
    throw5 INTEGER NOT NULL,
    throw6 INTEGER NOT NULL,
    throw7 INTEGER NOT NULL,
    throw8 INTEGER NOT NULL,
    total INTEGER NOT NULL,
    win BOOLEAN NOT NULL
);

INSERT INTO scores (competitor_id, match_id, quick_points, sequence, throw1, throw2, throw3, throw4, throw5, throw6, throw7, throw8, total, win)
    VALUES (1, 1, 2, 'ORANGE D (Bottom Right),BLUE C (Bottom Left),RED A (Top Left),GREEN B (Top Right),RED A (Top Left),GREEN B (Top Right),ORANGE D (Bottom Right),BLUE C (Bottom Left)', 2, 4, 2, 4, 2, 4, 2, 4, 25, TRUE),
    (2, 1, 4, 'ORANGE D (Bottom Right),BLUE C (Bottom Left),RED A (Top Left),GREEN B (Top Right),RED A (Top Left),GREEN B (Top Right),ORANGE D (Bottom Right),BLUE C (Bottom Left)',1, 8, 1, 8, 1, 8, 1, 8, 40, TRUE);