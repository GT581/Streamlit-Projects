with rnk as (
    select stcs.*,
        RANK() OVER (
            PARTITION BY stcs.dk_match_id
            ORDER BY stcs.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.soccer_total_corners_stage stcs
    join sports.draftkings.soccer_events se on stcs.dk_match_id = se.dk_match_id
    where se.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.soccer_total_corners (
        dk_match_id,
        dk_league_id,
        league,
        total_corners_under_odds,
        total_corners_line,
        total_corners_over_odds,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    total_corners_under_odds,
    total_corners_line,
    total_corners_over_odds,
    db_ts
FROM rnk
where timeRnk = 1 ON CONFLICT (dk_match_id) DO
UPDATE
SET dk_match_id = EXCLUDED.dk_match_id,
    dk_league_id = EXCLUDED.dk_league_id,
    league = EXCLUDED.league,
    total_corners_under_odds = EXCLUDED.total_corners_under_odds,
    total_corners_line = EXCLUDED.total_corners_line,
    total_corners_over_odds = EXCLUDED.total_corners_over_odds,
    db_ts = EXCLUDED.db_ts