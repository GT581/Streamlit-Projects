with rnk as (
    select sss.*,
        RANK() OVER (
            PARTITION BY sss.sofa_match_id,
            sss.streak_name,
            sss.streak_label,
            sss.hth_ind
            ORDER BY sss.db_ts DESC
        ) AS timeRnk
    from sports.sofascore.soccer_streaks_stage sss
        --join sports.sofascore.soccer_events se on sss.sofa_match_id = se.sofa_match_id
    --where se.match_dtime > CURRENT_TIMESTAMP AT TIME ZONE 'EST'
)
INSERT INTO sports.sofascore.soccer_streaks (
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