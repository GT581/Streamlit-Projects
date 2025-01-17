create view streaks_screener.soccer_total_corners as (
    select league,
        home_team,
        away_team,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        total_corners_under_odds,
        total_corners_line,
        total_corners_over_odds,
        match_dtime
    from streaks_screener.soccer
    where streak_category = 'total_corners'
        and match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)