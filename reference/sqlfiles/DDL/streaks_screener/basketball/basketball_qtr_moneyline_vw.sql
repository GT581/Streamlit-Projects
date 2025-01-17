create view streaks_screener.basketball_qtr_moneyline as (
    select league,
        home_team,
        away_team,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        home_qtr_odds,
        away_qtr_odds,
        match_dtime
    from streaks_screener.basketball
    where streak_category = 'qtr_moneyline'
        and match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)