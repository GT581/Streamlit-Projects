# import Pipelines.sports_common as sc
# from sqlalchemy import Integer, Text, DateTime, Numeric


# def writeDkSoccerEvents(df, table):
#     dbSchema = 'draftkings'
#     sport = 'soccer'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     'home_team': Text,
#     'away_team': Text,
#     'dk_home_team_id': Integer,
#     'dk_away_team_id': Integer,
#     'match_dtime': DateTime,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)


# def writeDkSoccerMoneyline(df, table):
#     dbSchema = 'draftkings'
#     sport = 'soccer'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     'home_team': Text,
#     'home_odds': Integer,
#     'draw_odds': Integer,
#     'away_odds': Integer,
#     'away_team': Text,
#     'dk_home_team_id': Integer,
#     'dk_away_team_id': Integer,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)


# def writeDkSoccerTotals(df, table):
#     dbSchema = 'draftkings'
#     sport = 'soccer'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     f'{table}_under_odds': Integer,
#     f'{table}_line': Numeric,
#     f'{table}_over_odds': Integer,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)


# def writeDkSoccerBtts(df, table):
#     dbSchema = 'draftkings'
#     sport = 'soccer'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     'btts_yes_odds': Integer,
#     'btts_no_odds': Integer,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)


# def writeDkSoccerFirstScore(df, table):
#     dbSchema = 'draftkings'
#     sport = 'soccer'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     'home_team': Text,
#     'home_first_score_odds': Integer,
#     'no_score_odds': Integer,
#     'away_first_score_odds': Integer,
#     'away_team': Text,
#     'dk_home_team_id': Integer,
#     'dk_away_team_id': Integer,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)


# def writeDkSoccerCleanSheet(df, table):
#     dbSchema = 'draftkings'
#     sport = 'soccer'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     'home_team': Text,
#     'home_cs_odds': Integer,
#     'home_no_cs_odds': Integer,
#     'away_team': Text,
#     'away_cs_odds': Integer,
#     'away_no_cs_odds': Integer,
#     'dk_home_team_id': Integer,
#     'dk_away_team_id': Integer,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)


# def writeDkSoccerHalfMoneyline(df, table):
#     dbSchema = 'draftkings'
#     sport = 'soccer'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     'home_team': Text,
#     'home_half_odds': Integer,
#     'draw_half_odds': Integer,
#     'away_half_odds': Integer,
#     'away_team': Text,
#     'dk_home_team_id': Integer,
#     'dk_away_team_id': Integer,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)