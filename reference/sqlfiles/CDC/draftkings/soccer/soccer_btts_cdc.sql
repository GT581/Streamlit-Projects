WITH rnk AS (
    SELECT sbs.*,
        RANK() OVER (
            PARTITION BY sbs.dk_match_id
            ORDER BY sbs.db_ts DESC
        ) AS timeRnk
    FROM sports.draftkings.soccer_btts_stage sbs
        join sports.draftkings.soccer_events se on sbs.dk_match_id = se.dk_match_id
    where se.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.soccer_btts (
        dk_match_id,
        dk_league_id,
        league,
        btts_yes_odds,
        btts_no_odds,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    btts_yes_odds,
    btts_no_odds,
    db_ts
FROM rnk
WHERE timeRnk = 1 ON CONFLICT (dk_match_id) DO
UPDATE
SET dk_match_id = EXCLUDED.dk_match_id,
    dk_league_id = EXCLUDED.dk_league_id,
    league = EXCLUDED.league,
    btts_yes_odds = EXCLUDED.btts_yes_odds,
    btts_no_odds = EXCLUDED.btts_no_odds,
    db_ts = EXCLUDED.db_ts