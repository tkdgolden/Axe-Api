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
            ('bob', 'berrymore');

CREATE TABLE seasons (
    season_id SERIAL PRIMARY KEY,
    season TEXT NOT NULL,
    start_date DATE NOT NULL
);

INSERT INTO seasons (season, start_date)
    VALUES ('I', '2024-01-20'),
            ('II', '2024-08-15');