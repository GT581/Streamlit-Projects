CREATE TABLE draftkings.soccer_total_corners (
	dk_match_id int4 NOT NULL,
	dk_league_id int4 NULL,
	league text NULL,
	total_corners_under_odds int4 NULL,
	total_corners_line numeric NULL,
	total_corners_over_odds int4 NULL,
	db_ts timestamp NULL,
	CONSTRAINT soccer_total_corners_pk PRIMARY KEY (dk_match_id)
);