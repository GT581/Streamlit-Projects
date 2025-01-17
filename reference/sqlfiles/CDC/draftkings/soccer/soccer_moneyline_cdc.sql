with rnk as (
    select sms.*,
        RANK() OVER (
            PARTITION BY sms.dk_match_id
            ORDER BY sms.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.soccer_moneyline_stage sms
        join sports.draftkings.soccer_events se on sms.dk_match_id = se.dk_match_id
    where se.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.soccer_moneyline (
        dk_match_id,
        dk_league_id,
        league,
        home_team,
        home_odds,
        draw_odds,
        away_odds,
        away_team,
        dk_home_team_id,
        dk_away_team_id,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    home_team,
    home_odds,
    draw_odds,
    away_odds,
    away_team,
    dk_home_team_id,
    dk_away_team_id,
    db_ts
FROM rnk
where timeRnk = 1 ON CONFLICT (dk_match_id) DO
UPDATE
SET dk_match_id = EXCLUDED.dk_match_id,
    dk_league_id = EXCLUDED.dk_league_id,
    league = EXCLUDED.league,
    home_team = EXCLUDED.home_team,
    home_odds = EXCLUDED.home_odds,
    draw_odds = EXCLUDED.draw_odds,
    away_odds = EXCLUDED.away_odds,
    away_team = EXCLUDED.away_team,
    dk_home_team_id = EXCLUDED.dk_home_team_id,
    dk_away_team_id = EXCLUDED.dk_away_team_id,
    db_ts = EXCLUDED.db_ts