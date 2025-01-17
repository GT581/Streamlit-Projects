create view streaks_screener.soccer_btts as (
    select league,
        home_team,
        away_team,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        btts_yes_odds,
        btts_no_odds,
        match_dtime
    from streaks_screener.soccer
    where streak_category = 'btts'
        and match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)