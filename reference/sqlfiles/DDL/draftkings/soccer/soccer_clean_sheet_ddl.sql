CREATE TABLE draftkings.soccer_clean_sheet (
	dk_match_id int4 NOT NULL,
	dk_league_id int4 NULL,
	league text NULL,
	home_team text NULL,
	home_cs_odds int4 NULL,
	home_no_cs_odds int4 NULL,
	away_team text NULL,
	away_cs_odds int4 NULL,
	away_no_cs_odds int4 NULL,
	dk_home_team_id int4 NULL,
	dk_away_team_id int4 NULL,
	db_ts timestamp NULL,
	CONSTRAINT soccer_clean_sheet_pk PRIMARY KEY (dk_match_id)
);