with rnk as (
    select shms.*,
        RANK() OVER (
            PARTITION BY shms.dk_match_id
            ORDER BY shms.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.soccer_half_moneyline_stage shms
        join sports.draftkings.soccer_events se on shms.dk_match_id = se.dk_match_id
    where se.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.soccer_half_moneyline (
        dk_match_id,
        dk_league_id,
        league,
        home_team,
        home_half_odds,
        draw_half_odds,
        away_half_odds,
        away_team,
        dk_home_team_id,
        dk_away_team_id,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    home_team,
    home_half_odds,
    draw_half_odds,
    away_half_odds,
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
    home_half_odds = EXCLUDED.home_half_odds,
    draw_half_odds = EXCLUDED.draw_half_odds,
    away_half_odds = EXCLUDED.away_half_odds,
    away_team = EXCLUDED.away_team,
    dk_home_team_id = EXCLUDED.dk_home_team_id,
    dk_away_team_id = EXCLUDED.dk_away_team_id,
    db_ts = EXCLUDED.db_ts