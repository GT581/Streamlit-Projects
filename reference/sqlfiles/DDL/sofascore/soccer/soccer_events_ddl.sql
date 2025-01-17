CREATE TABLE sofascore.soccer_events (
	sofa_match_id int4 NOT NULL,
	league text NULL,
	season text NULL,
	home_team text NULL,
	away_team text NULL,
	sofa_home_team_id int4 NULL,
	sofa_away_team_id int4 NULL,
	match_dtime timestamp NULL,
	db_ts timestamp NULL,
	CONSTRAINT soccer_events_pk PRIMARY KEY (sofa_match_id)
);