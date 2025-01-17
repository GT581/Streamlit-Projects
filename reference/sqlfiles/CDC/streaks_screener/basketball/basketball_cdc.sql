with matched_events as (
    SELECT distinct sbe.sofa_match_id,
        dbe.dk_match_id,
        dbe.league,
        bmh.team as home_team,
        bma.team as away_team,
        dbe.match_dtime
    FROM sports.sofascore.basketball_events sbe
        join sports.streaks_screener.basketball_mapping bmh on bmh.sofa_team_id = sbe.sofa_home_team_id
        join sports.streaks_screener.basketball_mapping bma on bma.sofa_team_id = sbe.sofa_away_team_id
        JOIN sports.draftkings.basketball_events dbe ON bmh.dk_team_id = dbe.dk_home_team_id
        and bma.dk_team_id = dbe.dk_away_team_id
        and date(dbe.match_dtime) = date(sbe.match_dtime)
    --where dbe.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
),
matched_streaks as (
    select me.sofa_match_id,
        me.dk_match_id,
        me.league,
        bs.streak_name,
        bs.streak_value,
        bs.streak_label,
        bs.hth_ind,
        bs.continued_ind,
        me.home_team,
        me.away_team,
        me.match_dtime
    from sports.sofascore.basketball_streaks bs
        join matched_events me on bs.sofa_match_id = me.sofa_match_id
)
insert into streaks_screener.basketball(
        sofa_match_id,
        dk_match_id,
        league,
        streak_category,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        continued_ind,
        home_team,
        away_team,
        match_dtime,
        home_odds,
        away_odds,
        home_half_odds,
        away_half_odds,
        home_qtr_odds,
        away_qtr_odds,
        home_spread,
        home_spread_odds,
        away_spread_odds,
        away_spread,
        total_points_under_odds,
        total_points_line,
        total_points_over_odds
    )
select ms.sofa_match_id,
    ms.dk_match_id,
    ms.league,
    case
        when ms.streak_name like 'Game points%' then 'total_points'
        when ms.streak_name like 'Scored points%' then 'total_points'
        when ms.streak_name like 'First quarter%' then 'qtr_moneyline'
        when ms.streak_name like 'First half%' then 'half_moneyline'
        when ms.streak_name like '%Wins' then 'moneyline'
        when ms.streak_name like '%Losses' then 'moneyline'
    end as streak_category,
    ms.streak_name,
    ms.streak_value,
    ms.streak_label,
    ms.hth_ind,
    ms.continued_ind,
    ms.home_team,
    ms.away_team,
    ms.match_dtime,
    bm.home_odds,
    bm.away_odds,
    bhm.home_half_odds,
    bhm.away_half_odds,
    bqm.home_qtr_odds,
    bqm.away_qtr_odds,
    bs.home_spread,
    bs.home_spread_odds,
    bs.away_spread_odds,
    bs.away_spread,
    btp.total_points_under_odds,
    btp.total_points_line,
    btp.total_points_over_odds
from matched_streaks ms
    left join sports.draftkings.basketball_moneyline bm on ms.dk_match_id = bm.dk_match_id
    left join sports.draftkings.basketball_half_moneyline bhm on ms.dk_match_id = bhm.dk_match_id
    left join sports.draftkings.basketball_qtr_moneyline bqm on ms.dk_match_id = bqm.dk_match_id
    left join sports.draftkings.basketball_spread bs on ms.dk_match_id = bs.dk_match_id
    left join sports.draftkings.basketball_total_points btp on ms.dk_match_id = btp.dk_match_id ON CONFLICT (
        sofa_match_id,
        dk_match_id,
        streak_name,
        streak_label,
        hth_ind
    ) DO
UPDATE
SET sofa_match_id = EXCLUDED.sofa_match_id,
    dk_match_id = EXCLUDED.dk_match_id,
    league = EXCLUDED.league,
    streak_category = EXCLUDED.streak_category,
    streak_name = EXCLUDED.streak_name,
    streak_value = EXCLUDED.streak_value,
    streak_label = EXCLUDED.streak_label,
    hth_ind = EXCLUDED.hth_ind,
    continued_ind = EXCLUDED.continued_ind,
    home_team = EXCLUDED.home_team,
    away_team = EXCLUDED.away_team,
    match_dtime = EXCLUDED.match_dtime,
    home_odds = EXCLUDED.home_odds,
    away_odds = EXCLUDED.away_odds,
    home_half_odds = EXCLUDED.home_half_odds,
    away_half_odds = EXCLUDED.away_half_odds,
    home_qtr_odds = EXCLUDED.home_qtr_odds,
    away_qtr_odds = EXCLUDED.away_qtr_odds,
    home_spread = EXCLUDED.home_spread,
    home_spread_odds = EXCLUDED.home_spread_odds,
    away_spread_odds = EXCLUDED.away_spread_odds,
    away_spread = EXCLUDED.away_spread,
    total_points_under_odds = EXCLUDED.total_points_under_odds,
    total_points_line = EXCLUDED.total_points_line,
    total_points_over_odds = EXCLUDED.total_points_over_odds