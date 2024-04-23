#Lists of schemas to filter, rename, and/or reorder our dataframes

def sofaMatches():
    schema = ['league', 'season', 'home_team', 'away_team', 'match_dtime']
    displaySchema = ['League', 'Season', 'Home Team', 'Away Team', 'Match Time']
    return schema, displaySchema


def sofaStreaks():
    schema = ['streak_category', 'streak_name', 'streak_value', 'streak_label', 'hth_ind']
    displaySchema = ['Streak Category', 'Streak Name', 'Streak Value', 'Streak Label', 'H2H']
    return schema, displaySchema


def sofaColumnsCommon():
    sofaSchema = ['home_team_x', 'away_team_x', 'streak_name', 'streak_value', 'streak_label', 'hth_ind']
    sofaTotalSchema = ['home_team', 'away_team', 'streak_name', 'streak_value', 'streak_label', 'hth_ind']
    sofaDisplaySchema = ['Home Team', 'Away Team', 'Streak Name', 'Streak Value', 'Streak Label', 'H2H']
    return sofaSchema, sofaTotalSchema, sofaDisplaySchema


def soccerMoneyline():
    schema = ['home_odds', 'draw_odds', 'away_odds', 'match_dtime']
    displaySchema = ['Home Odds', 'Draw Odds', 'Away Odds', 'Match Time']
    return schema, displaySchema


def soccerHalfMoneyline():
    schema = ['home_half_odds', 'draw_half_odds', 'away_half_odds', 'match_dtime']
    displaySchema = ['Home First Half Odds', 'Draw First Half Odds', 'Away First Half Odds', 'Match Time']
    return schema, displaySchema


def btts():
    schema = ['btts_yes_odds', 'btts_no_odds', 'match_dtime']
    displaySchema = ['Both Teams to Score', 'Both Teams not to Score', 'Match Time']
    return schema, displaySchema


def cleanSheet():
    schema = ['home_cs_odds', 'away_cs_odds', 'home_no_cs_odds', 'away_no_cs_odds','match_dtime']
    displaySchema = ['Home Clean Sheet Odds', 'Away Clean Sheet Odds', 'Home No Clean Sheet Odds', 'Away No Clean Sheet Odds', 'Match Time']
    return schema, displaySchema


def firstScore():
    schema = ['home_first_score_odds', 'no_score_odds', 'away_first_score_odds', 'match_dtime']
    displaySchema = ['Home First to Score Odds', 'No Goals Scored Odds', 'Away First to Score Odds', 'Match Time']
    return schema, displaySchema


def totalCards():
    schema = ['total_cards_under_odds', 'total_cards_line', 'total_cards_over_odds', 'match_dtime']
    displaySchema = ['Total Cards Under Odds', 'Total Cards Line', 'Total Cards Over Odds', 'Match Time']
    return schema, displaySchema


def totalCorners():
    schema = ['total_corners_under_odds', 'total_corners_line', 'total_corners_over_odds', 'match_dtime']
    displaySchema = ['Total Corners Under Odds', 'Total Corners Line', 'Total Corners Over Odds', 'Match Time']
    return schema, displaySchema


def totalGoals():
    schema = ['total_goals_under_odds', 'total_goals_line', 'total_goals_over_odds', 'match_dtime']
    displaySchema = ['Total Goals Under Odds', 'Total Goals Line', 'Total Goals Over Odds', 'Match Time']
    return schema, displaySchema


def basketballMoneyline():
    schema = ['home_odds', 'away_odds', 'match_dtime']
    displaySchema = ['Home Odds', 'Away Odds', 'Match Time']
    return schema, displaySchema


def basketballHalfMoneyline():
    schema = ['home_half_odds', 'away_half_odds', 'match_dtime']
    displaySchema = ['Home First Half Odds', 'Away First Half Odds', 'Match Time']
    return schema, displaySchema


def qtrMoneyline():
    schema = ['home_qtr_odds', 'away_qtr_odds', 'match_dtime']
    displaySchema = ['Home First Qtr Odds', 'Away First Qtr Odds', 'Match Time']
    return schema, displaySchema


def totalPoints():
    schema = ['total_points_under_odds', 'total_points_line', 'total_points_over_odds', 'match_dtime']
    displaySchema = ['Total Points Under Odds', 'Total Points Line', 'Total Points Over Odds', 'Match Time']
    return schema, displaySchema