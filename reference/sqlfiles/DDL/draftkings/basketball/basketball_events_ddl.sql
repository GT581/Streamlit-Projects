CREATE TABLE draftkings.basketball_events (
	dk_match_id int4 NOT NULL,
	dk_league_id int4 NULL,
	league text NULL,
	home_team text NULL,
	away_team text NULL,
	dk_home_team_id int4 NULL,
	dk_away_team_id int4 NULL,
	match_dtime timestamp NULL,
	db_ts timestamp NULL,
	CONSTRAINT basketball_events_pk PRIMARY KEY (dk_match_id)
);