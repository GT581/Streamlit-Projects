with rnk as (
    select stgs.*,
        RANK() OVER (
            PARTITION BY stgs.dk_match_id
            ORDER BY stgs.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.soccer_total_goals_stage stgs
        join sports.draftkings.soccer_events se on stgs.dk_match_id = se.dk_match_id
    where se.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.soccer_total_goals (
        dk_match_id,
        dk_league_id,
        league,
        total_goals_under_odds,
        total_goals_line,
        total_goals_over_odds,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    total_goals_under_odds,
    total_goals_line,
    total_goals_over_odds,
    db_ts
FROM rnk
where timeRnk = 1 ON CONFLICT (dk_match_id) DO
UPDATE
SET dk_match_id = EXCLUDED.dk_match_id,
    dk_league_id = EXCLUDED.dk_league_id,
    league = EXCLUDED.league,
    total_goals_under_odds = EXCLUDED.total_goals_under_odds,
    total_goals_line = EXCLUDED.total_goals_line,
    total_goals_over_odds = EXCLUDED.total_goals_over_odds,
    db_ts = EXCLUDED.db_ts