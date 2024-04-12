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
    VALUES ('judge1', 'pAsSwOrD');

CREATE TABLE competitors (
    competitor_id SERIAL PRIMARY KEY,
    competitor_first_name TEXT NOT NULL,
    competitor_last_name TEXT NOT NULL
);

INSERT INTO competitors (competitor_first_name, competitor_last_name)
    VALUES ('ann', 'applewood'),
            ('bob', 'berrymore');