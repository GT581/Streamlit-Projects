with rnk as (
    select *,
        RANK() OVER (
            PARTITION BY dk_match_id
            ORDER BY db_ts DESC
        ) AS timeRnk
    from sports.draftkings.soccer_events_stage
    where match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.soccer_events (
        dk_match_id,
        dk_league_id,
        league,
        home_team,
        away_team,
        dk_home_team_id,
        dk_away_team_id,
        match_dtime,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    home_team,
    away_team,
    dk_home_team_id,
    dk_away_team_id,
    match_dtime,
    db_ts
FROM rnk
where timeRnk = 1 ON CONFLICT (dk_match_id) DO
UPDATE
SET dk_match_id = EXCLUDED.dk_match_id,
    dk_league_id = EXCLUDED.dk_league_id,
    league = EXCLUDED.league,
    home_team = EXCLUDED.home_team,
    away_team = EXCLUDED.away_team,
    dk_home_team_id = EXCLUDED.dk_home_team_id,
    dk_away_team_id = EXCLUDED.dk_away_team_id,
    match_dtime = EXCLUDED.match_dtime,
    db_ts = EXCLUDED.db_ts