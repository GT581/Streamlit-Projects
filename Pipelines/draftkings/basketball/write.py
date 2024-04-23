# import Pipelines.sports_common as sc
# from sqlalchemy import Integer, Text, DateTime, Numeric


# def writeDkBasketballEvents(df, table):
#     dbSchema = 'draftkings'
#     sport = 'basketball'
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


# def writeDkBasketballMoneyline(df, table):
#     dbSchema = 'draftkings'
#     sport = 'basketball'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     'home_team': Text,
#     'home_odds': Integer,
#     'away_odds': Integer,
#     'away_team': Text,
#     'dk_home_team_id': Integer,
#     'dk_away_team_id': Integer,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)


# def writeDkBasketballSpreads(df, table):
#     dbSchema = 'draftkings'
#     sport = 'basketball'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     'home_team': Text,
#     'home_spread': Numeric,
#     'home_spread_odds': Integer,
#     'away_spread_odds': Integer,
#     'away_spread': Numeric,
#     'away_odds': Integer,
#     'away_team': Text,
#     'dk_home_team_id': Integer,
#     'dk_away_team_id': Integer,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)


# def writeDkBasketballTotals(df, table):
#     dbSchema = 'draftkings'
#     sport = 'basketball'
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


# def writeDkBasketballHalfMoneyline(df, table):
#     dbSchema = 'draftkings'
#     sport = 'basketball'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     'home_team': Text,
#     'home_half_odds': Integer,
#     'away_half_odds': Integer,
#     'away_team': Text,
#     'dk_home_team_id': Integer,
#     'dk_away_team_id': Integer,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)


# def writeDkBasketballQtrMoneyline(df, table):
#     dbSchema = 'draftkings'
#     sport = 'basketball'
#     schema = {
#     'dk_match_id': Integer,
#     'dk_league_id': Integer,
#     'league': Text,
#     'home_team': Text,
#     'home_qtr_odds': Integer,
#     'away_qtr_odds': Integer,
#     'away_team': Text,
#     'dk_home_team_id': Integer,
#     'dk_away_team_id': Integer,
#     'db_ts': DateTime
#     }
#     sc.writeStage(df, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)