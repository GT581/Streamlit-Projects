with rnk as (
    select bqms.*,
        RANK() OVER (
            PARTITION BY bqms.dk_match_id
            ORDER BY bqms.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.basketball_qtr_moneyline_stage bqms
        join sports.draftkings.basketball_events be on bqms.dk_match_id = be.dk_match_id
    where be.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.basketball_qtr_moneyline (
        dk_match_id,
        dk_league_id,
        league,
        home_team,
        home_qtr_odds,
        away_qtr_odds,
        away_team,
        dk_home_team_id,
        dk_away_team_id,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    home_team,
    home_qtr_odds,
    away_qtr_odds,
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
    home_qtr_odds = EXCLUDED.home_qtr_odds,
    away_qtr_odds = EXCLUDED.away_qtr_odds,
    away_team = EXCLUDED.away_team,
    dk_home_team_id = EXCLUDED.dk_home_team_id,
    dk_away_team_id = EXCLUDED.dk_away_team_id,
    db_ts = EXCLUDED.db_ts