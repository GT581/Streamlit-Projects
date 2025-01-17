with rnk as (
    select *,
        RANK() OVER (
            PARTITION BY sofa_match_id
            ORDER BY db_ts DESC
        ) AS timeRnk
    from sports.sofascore.basketball_events_stage
    where match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.sofascore.basketball_events (
        sofa_match_id,
        league,
        season,
        home_team,
        away_team,
        sofa_home_team_id,
        sofa_away_team_id,
        match_dtime,
        db_ts
    )
SELECT sofa_match_id,
    league,
    season,
    home_team,
    away_team,
    sofa_home_team_id,
    sofa_away_team_id,
    match_dtime,
    db_ts
FROM rnk
where timeRnk = 1 ON CONFLICT (sofa_match_id) DO
UPDATE
SET sofa_match_id = EXCLUDED.sofa_match_id,
    league = EXCLUDED.league,
    season = EXCLUDED.season,
    home_team = EXCLUDED.home_team,
    away_team = EXCLUDED.away_team,
    sofa_home_team_id = EXCLUDED.sofa_home_team_id,
    sofa_away_team_id = EXCLUDED.sofa_away_team_id,
    db_ts = EXCLUDED.db_ts