with rnk as (
    select stcs.*,
        RANK() OVER (
            PARTITION BY stcs.dk_match_id
            ORDER BY stcs.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.soccer_total_cards_stage stcs
        join sports.draftkings.soccer_events se on stcs.dk_match_id = se.dk_match_id
    where se.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.soccer_total_cards (
        dk_match_id,
        dk_league_id,
        league,
        total_cards_under_odds,
        total_cards_line,
        total_cards_over_odds,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    total_cards_under_odds,
    total_cards_line,
    total_cards_over_odds,
    db_ts
FROM rnk
where timeRnk = 1 ON CONFLICT (dk_match_id) DO
UPDATE
SET dk_match_id = EXCLUDED.dk_match_id,
    dk_league_id = EXCLUDED.dk_league_id,
    league = EXCLUDED.league,
    total_cards_under_odds = EXCLUDED.total_cards_under_odds,
    total_cards_line = EXCLUDED.total_cards_line,
    total_cards_over_odds = EXCLUDED.total_cards_over_odds,
    db_ts = EXCLUDED.db_ts