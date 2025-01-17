create view streaks_screener.soccer_first_score as (
    select league,
        home_team,
        away_team,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        home_first_score_odds,
        no_score_odds,
        away_first_score_odds,
        match_dtime
    from streaks_screener.soccer
    where streak_category = 'first_score'
        and match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)