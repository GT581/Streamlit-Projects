create view streaks_screener.soccer_moneyline as (
    select league,
        home_team,
        away_team,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        home_odds,
        draw_odds,
        away_odds,
        match_dtime
    from streaks_screener.soccer
    where streak_category = 'moneyline'
        and match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)