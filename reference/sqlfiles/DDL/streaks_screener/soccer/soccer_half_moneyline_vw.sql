create view streaks_screener.soccer_half_moneyline as (
    select league,
        home_team,
        away_team,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        home_half_odds,
        draw_half_odds,
        away_half_odds,
        match_dtime
    from streaks_screener.soccer
    where streak_category = 'half_moneyline'
        and match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)