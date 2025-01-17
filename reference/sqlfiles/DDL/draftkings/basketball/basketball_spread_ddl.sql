CREATE TABLE draftkings.basketball_spread (
	dk_match_id int4 NOT NULL,
	dk_league_id int4 NULL,
	league text NULL,
	home_team text NULL,
	home_spread numeric NULL,
	home_spread_odds int4 NULL,
	away_spread_odds int4 NULL,
	away_spread numeric NULL,
	away_team text NULL,
	dk_home_team_id int4 NULL,
	dk_away_team_id int4 NULL,
	db_ts timestamp NULL,
    CONSTRAINT basketball_spread_pk PRIMARY KEY (dk_match_id)
);