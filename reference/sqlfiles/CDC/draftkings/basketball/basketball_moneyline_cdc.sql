with rnk as (
    select bms.*,
        RANK() OVER (
            PARTITION BY bms.dk_match_id
            ORDER BY bms.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.basketball_moneyline_stage bms
        join sports.draftkings.basketball_events be on bms.dk_match_id = be.dk_match_id
    where be.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.basketball_moneyline (
        dk_match_id,
        dk_league_id,
        league,
        home_team,
        home_odds,
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
    away_odds = EXCLUDED.away_odds,
    away_team = EXCLUDED.away_team,
    dk_home_team_id = EXCLUDED.dk_home_team_id,
    dk_away_team_id = EXCLUDED.dk_away_team_id,
    db_ts = EXCLUDED.db_ts