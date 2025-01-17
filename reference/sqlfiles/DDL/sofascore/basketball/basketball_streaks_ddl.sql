CREATE TABLE sofascore.basketball_streaks (
	sofa_match_id int4 NOT NULL,
	league text NULL,
	streak_name text NOT NULL,
	streak_value text NULL,
	streak_label text NOT NULL,
	hth_ind bool NOT NULL,
	continued_ind bool NULL,
	db_ts timestamp NULL,
	CONSTRAINT basketball_streaks_pk PRIMARY KEY (
		sofa_match_id,
		streak_name,
		streak_label,
		hth_ind
	)
);