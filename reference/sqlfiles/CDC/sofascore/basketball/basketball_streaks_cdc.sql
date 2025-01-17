with rnk as (
    select bss.*,
        RANK() OVER (
            PARTITION BY bss.sofa_match_id,
            bss.streak_name,
            bss.streak_label,
            bss.hth_ind
            ORDER BY bss.db_ts DESC
        ) AS timeRnk
    from sports.sofascore.basketball_streaks_stage bss
        --join sports.sofascore.basketball_events be on bss.sofa_match_id = be.sofa_match_id
    --where be.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.sofascore.basketball_streaks (
        sofa_match_id,
        league,
        streak_name,
        streak_value,
        streak_label,
        hth_ind,
        continued_ind,
        db_ts
    )
SELECT sofa_match_id,
    league,
    streak_name,
    streak_value,
    streak_label,
    hth_ind,
    continued_ind,
    db_ts
FROM rnk
where timeRnk = 1 ON CONFLICT (
        sofa_match_id,
        streak_name,
        streak_label,
        hth_ind
    ) DO
UPDATE
SET sofa_match_id = EXCLUDED.sofa_match_id,
    league = EXCLUDED.league,
    streak_name = EXCLUDED.streak_name,
    streak_value = EXCLUDED.streak_value,
    streak_label = EXCLUDED.streak_label,
    hth_ind = EXCLUDED.hth_ind,
    continued_ind = EXCLUDED.continued_ind,
    db_ts = EXCLUDED.db_ts