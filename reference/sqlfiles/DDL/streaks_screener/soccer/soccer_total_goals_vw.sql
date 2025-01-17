create view streaks_screener.soccer_total_goals as (
    select league,
        home_team,
        away_team,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        total_goals_under_odds,
        total_goals_line,
        total_goals_over_odds,
        match_dtime
    from streaks_screener.soccer
    where streak_category = 'total_goals'
        and match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)