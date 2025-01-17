create view streaks_screener.soccer_total_cards as (
    select league,
        home_team,
        away_team,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        total_cards_under_odds,
        total_cards_line,
        total_cards_over_odds,
        match_dtime
    from streaks_screener.soccer
    where streak_category = 'total_cards'
        and match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)