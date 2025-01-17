CREATE TABLE draftkings.soccer_btts (
	dk_match_id int4 NOT NULL,
	dk_league_id int4 NULL,
	league text NULL,
	btts_yes_odds int4 NULL,
	btts_no_odds int4 NULL,
	db_ts timestamp NULL,
	CONSTRAINT soccer_btts_pk PRIMARY KEY (dk_match_id)
);