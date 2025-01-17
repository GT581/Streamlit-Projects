with rnk as (
    select scss.*,
        RANK() OVER (
            PARTITION BY scss.dk_match_id
            ORDER BY scss.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.soccer_clean_sheet_stage scss
        join sports.draftkings.soccer_events se on scss.dk_match_id = se.dk_match_id
    where se.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.soccer_clean_sheet (
        dk_match_id,
        dk_league_id,
        league,
        home_team,
        home_cs_odds,
        home_no_cs_odds,
        away_team,
        away_cs_odds,
        away_no_cs_odds,
        dk_home_team_id,
        dk_away_team_id,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    home_team,
    home_cs_odds,
    home_no_cs_odds,
    away_team,
    away_cs_odds,
    away_no_cs_odds,
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
    home_cs_odds = EXCLUDED.home_cs_odds,
    home_no_cs_odds = EXCLUDED.home_no_cs_odds,
    away_team = EXCLUDED.away_team,
    away_cs_odds = EXCLUDED.away_cs_odds,
    away_no_cs_odds = EXCLUDED.away_no_cs_odds,
    dk_home_team_id = EXCLUDED.dk_home_team_id,
    dk_away_team_id = EXCLUDED.dk_away_team_id,
    db_ts = EXCLUDED.db_ts