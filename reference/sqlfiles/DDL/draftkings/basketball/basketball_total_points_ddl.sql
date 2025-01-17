CREATE TABLE draftkings.basketball_total_points (
	dk_match_id int4 NOT NULL,
	dk_league_id int4 NULL,
	league text NULL,
	total_points_under_odds int4 NULL,
	total_points_line numeric NULL,
	total_points_over_odds int4 NULL,
	db_ts timestamp NULL,
	CONSTRAINT basketball_total_points_pk PRIMARY KEY (dk_match_id)
);