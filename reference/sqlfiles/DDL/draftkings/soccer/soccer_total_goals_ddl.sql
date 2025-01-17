CREATE TABLE draftkings.soccer_total_goals (
	dk_match_id int4 NOT NULL,
	dk_league_id int4 NULL,
	league text NULL,
	total_goals_under_odds int4 NULL,
	total_goals_line numeric NULL,
	total_goals_over_odds int4 NULL,
	db_ts timestamp NULL,
	CONSTRAINT soccer_total_goals_pk PRIMARY KEY (dk_match_id)
);