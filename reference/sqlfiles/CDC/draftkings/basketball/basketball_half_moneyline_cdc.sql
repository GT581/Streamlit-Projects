with rnk as (
    select bhms.*,
        RANK() OVER (
            PARTITION BY bhms.dk_match_id
            ORDER BY bhms.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.basketball_half_moneyline_stage bhms
        join sports.draftkings.basketball_events be on bhms.dk_match_id = be.dk_match_id
    where be.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.basketball_half_moneyline (
        dk_match_id,
        dk_league_id,
        league,
        home_team,
        home_half_odds,
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
    away_half_odds = EXCLUDED.away_half_odds,
    away_team = EXCLUDED.away_team,
    dk_home_team_id = EXCLUDED.dk_home_team_id,
    dk_away_team_id = EXCLUDED.dk_away_team_id,
    db_ts = EXCLUDED.db_ts