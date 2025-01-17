with rnk as (
    select sfss.*,
        RANK() OVER (
            PARTITION BY sfss.dk_match_id
            ORDER BY sfss.db_ts DESC
        ) AS timeRnk
    from sports.draftkings.soccer_first_score_stage sfss
        join sports.draftkings.soccer_events se on sfss.dk_match_id = se.dk_match_id
    where se.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.draftkings.soccer_first_score (
        dk_match_id,
        dk_league_id,
        league,
        home_team,
        home_first_score_odds,
        no_score_odds,
        away_first_score_odds,
        away_team,
        dk_home_team_id,
        dk_away_team_id,
        db_ts
    )
SELECT dk_match_id,
    dk_league_id,
    league,
    home_team,
    home_first_score_odds,
    no_score_odds,
    away_first_score_odds,
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
    home_first_score_odds = EXCLUDED.home_first_score_odds,
    no_score_odds = EXCLUDED.no_score_odds,
    away_first_score_odds = EXCLUDED.away_first_score_odds,
    away_team = EXCLUDED.away_team,
    dk_home_team_id = EXCLUDED.dk_home_team_id,
    dk_away_team_id = EXCLUDED.dk_away_team_id,
    db_ts = EXCLUDED.db_ts