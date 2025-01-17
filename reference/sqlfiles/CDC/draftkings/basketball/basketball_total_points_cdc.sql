with rnk as (
    select btps.*,
        RANK() OVER (
            PARTITION BY btps.dk_match_id
            ORDER BY btps.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.basketball_total_points_stage btps
        join sports.draftkings.basketball_events be on btps.dk_match_id = be.dk_match_id
    where be.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.basketball_total_points (
        dk_match_id,
        dk_league_id,
        league,
        total_points_under_odds,
        total_points_line,
        total_points_over_odds,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    total_points_under_odds,
    total_points_line,
    total_points_over_odds,
    db_ts
FROM rnk
where timeRnk = 1 ON CONFLICT (dk_match_id) DO
UPDATE
SET dk_match_id = EXCLUDED.dk_match_id,
    dk_league_id = EXCLUDED.dk_league_id,
    league = EXCLUDED.league,
    total_points_under_odds = EXCLUDED.total_points_under_odds,
    total_points_line = EXCLUDED.total_points_line,
    total_points_over_odds = EXCLUDED.total_points_over_odds,
    db_ts = EXCLUDED.db_ts