create view streaks_screener.soccer_clean_sheet as (
    select league,
        home_team,
        away_team,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        home_cs_odds,
        away_cs_odds,
        home_no_cs_odds,
        away_no_cs_odds,
        match_dtime
    from streaks_screener.soccer
    where streak_category = 'clean_sheet'
        and match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)