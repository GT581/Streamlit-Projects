with matched_events as (
	SELECT distinct sse.sofa_match_id,
		dse.dk_match_id,
		dse.league,
		smh.team as home_team,
		sma.team as away_team,
		dse.match_dtime
	FROM sports.sofascore.soccer_events sse
		join sports.streaks_screener.soccer_mapping smh on smh.sofa_team_id = sse.sofa_home_team_id
		join sports.streaks_screener.soccer_mapping sma on sma.sofa_team_id = sse.sofa_away_team_id
		JOIN sports.draftkings.soccer_events dse ON smh.dk_team_id = dse.dk_home_team_id
		and sma.dk_team_id = dse.dk_away_team_id
		and date(sse.match_dtime) = date(dse.match_dtime)
	--where dse.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
),
matched_streaks as (
	select me.sofa_match_id,
		me.dk_match_id,
		me.league,
		ss.streak_name,
		ss.streak_value,
		ss.streak_label,
		ss.hth_ind,
		ss.continued_ind,
		me.home_team,
		me.away_team,
		me.match_dtime
	from sports.sofascore.soccer_streaks ss
		join matched_events me on ss.sofa_match_id = me.sofa_match_id
)
insert into streaks_screener.soccer(
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
		draw_odds,
		away_odds,
		home_half_odds,
		draw_half_odds,
		away_half_odds,
		total_goals_under_odds,
		total_goals_line,
		total_goals_over_odds,
		home_first_score_odds,
		no_score_odds,
		away_first_score_odds,
		btts_yes_odds,
		btts_no_odds,
		home_cs_odds,
		away_cs_odds,
		home_no_cs_odds,
		away_no_cs_odds,
		total_corners_under_odds,
		total_corners_line,
		total_corners_over_odds,
		total_cards_under_odds,
		total_cards_line,
		total_cards_over_odds
	)
select ms.sofa_match_id,
	ms.dk_match_id,
	ms.league,
	case
		when ms.streak_name like '%cards' then 'total_cards'
		when ms.streak_name like '%.5 goals' then 'total_goals'
		when ms.streak_name like '%.5 corners' then 'total_corners'
		when ms.streak_name like 'First to%' then 'first_score'
		when ms.streak_name like '%half%' then 'half_moneyline'
		when ms.streak_name like '%wins' then 'moneyline'
		when ms.streak_name like '%losses' then 'moneyline'
		when ms.streak_name like '%Wins' then 'moneyline'
		when ms.streak_name like '%Losses' then 'moneyline'
		when ms.streak_name like '%clean sheet' then 'clean_sheet'
		when ms.streak_name like '%conceded' then 'clean_sheet'
		when ms.streak_name like 'Both%' then 'btts'
		when ms.streak_name like '%scored' then 'clean_sheet'
		else NULL
	end as streak_category,
	ms.streak_name,
	ms.streak_value,
	ms.streak_label,
	ms.hth_ind,
	ms.continued_ind,
	ms.home_team,
	ms.away_team,
	ms.match_dtime,
	sm.home_odds,
	sm.draw_odds,
	sm.away_odds,
	shm.home_half_odds,
	shm.draw_half_odds,
	shm.away_half_odds,
	stg.total_goals_under_odds,
	stg.total_goals_line,
	stg.total_goals_over_odds,
	sfs.home_first_score_odds,
	sfs.no_score_odds,
	sfs.away_first_score_odds,
	sb.btts_yes_odds,
	sb.btts_no_odds,
	scs.home_cs_odds,
	scs.away_cs_odds,
	scs.home_no_cs_odds,
	scs.away_no_cs_odds,
	stco.total_corners_under_odds,
	stco.total_corners_line,
	stco.total_corners_over_odds,
	stca.total_cards_under_odds,
	stca.total_cards_line,
	stca.total_cards_over_odds
from matched_streaks ms
	left join sports.draftkings.soccer_moneyline sm on ms.dk_match_id = sm.dk_match_id
	left join sports.draftkings.soccer_half_moneyline shm on ms.dk_match_id = shm.dk_match_id
	left join sports.draftkings.soccer_total_goals stg on ms.dk_match_id = stg.dk_match_id
	left join sports.draftkings.soccer_first_score sfs on ms.dk_match_id = sfs.dk_match_id
	left join sports.draftkings.soccer_btts sb on ms.dk_match_id = sb.dk_match_id
	left join sports.draftkings.soccer_clean_sheet scs on ms.dk_match_id = scs.dk_match_id
	left join sports.draftkings.soccer_total_corners stco on ms.dk_match_id = stco.dk_match_id
	left join sports.draftkings.soccer_total_cards stca on ms.dk_match_id = stca.dk_match_id ON CONFLICT (
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
	draw_odds = EXCLUDED.draw_odds,
	away_odds = EXCLUDED.away_odds,
	home_half_odds = EXCLUDED.home_half_odds,
	draw_half_odds = EXCLUDED.draw_half_odds,
	away_half_odds = EXCLUDED.away_half_odds,
	total_goals_under_odds = EXCLUDED.total_goals_under_odds,
	total_goals_line = EXCLUDED.total_goals_line,
	total_goals_over_odds = EXCLUDED.total_goals_over_odds,
	home_first_score_odds = EXCLUDED.home_first_score_odds,
	no_score_odds = EXCLUDED.no_score_odds,
	away_first_score_odds = EXCLUDED.away_first_score_odds,
	btts_yes_odds = EXCLUDED.btts_yes_odds,
	btts_no_odds = EXCLUDED.btts_no_odds,
	home_cs_odds = EXCLUDED.home_cs_odds,
	away_cs_odds = EXCLUDED.away_cs_odds,
	home_no_cs_odds = EXCLUDED.home_no_cs_odds,
	away_no_cs_odds = EXCLUDED.away_no_cs_odds,
	total_corners_under_odds = EXCLUDED.total_corners_under_odds,
	total_corners_line = EXCLUDED.total_corners_line,
	total_corners_over_odds = EXCLUDED.total_corners_over_odds,
	total_cards_under_odds = EXCLUDED.total_cards_under_odds,
	total_cards_line = EXCLUDED.total_cards_line,
	total_cards_over_odds = EXCLUDED.total_cards_over_odds