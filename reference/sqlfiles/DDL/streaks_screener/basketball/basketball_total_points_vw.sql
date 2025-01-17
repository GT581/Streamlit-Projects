create view streaks_screener.basketball_total_points as (
    select league,
        home_team,
        away_team,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        total_points_under_odds,
        total_points_line,
        total_points_over_odds,
        match_dtime
    from streaks_screener.basketball
    where streak_category = 'total_points'
        and match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)