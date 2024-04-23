import numpy as np
from App.streaks import schemas


def dkSofaLeagueMapping(sport, sofaLeague):
    '''
    Dict to match sofascore leagues to draftkings leagues

    Args:
        sport: string of sport name
        sofaLeague: string of sofascore league name

    Returns:
        dkLeague: draftkings league name
    '''

    mapDict = {
    "hockey": {
        "NHL": "NHL"
    },
    #"football": [{"eventGroup": "88808"}], #NFL
    "basketball": {
        "NBA": "NBA",
        "NBA, Play-IN Tournament": "NBA",
        "NBA, Playoffs": "NBA",
        #"NCAA Men": "NCAAM",
        "NCAA Division I, Championship": "NCAAM"
        },
    #"baseball": [{"eventGroup": "84240"}], #MLB
    "soccer": {
        "Premier League": "England - Premier League",
        "LaLiga": "Spain - La Liga",
        "Serie A": "Italy - Serie A",
        "Bundesliga": "Germany - Bundesliga",
        "Ligue 1": "France - Ligue 1",
        "UEFA Champions League, Knockout stage": "Champions League",
        "UEFA Europa League, Knockout stage": "Europa League",
        "MLS": "USA - MLS" 
        }
    }
    dkLeague = mapDict[sport][sofaLeague]

    return dkLeague


def configSoccerStreakCats(streakDf):
    '''
    Adds soccer streak category to streaks dataframe based on streak name patterns

    Args:
        streakDf: dataframe of sofascore soccer streaks

    Returns:
        streakDf: dataframe of sofascore soccer streaks with streak category column
    '''

    streakDf['streak_name'] = streakDf['streak_name'].astype(str)

    conditions = [
        streakDf['streak_name'].str.contains('cards'),
        streakDf['streak_name'].str.contains('.5 goals'),
        streakDf['streak_name'].str.contains('.5 corners'),
        streakDf['streak_name'].str.startswith('First to'),
        streakDf['streak_name'].str.contains('half'),
        streakDf['streak_name'].str.contains('wins|losses|Wins|Losses'),
        #streakDf['streak_name'].str.contains('clean sheet|conceded|scored'),
        streakDf['streak_name'].str.contains('Both'),
    ]

    values = [
        'total_cards',
        'total_goals',
        'total_corners',
        'first_score',
        'half_moneyline',
        'moneyline',
        #'clean_sheet',
        'btts',
    ]

    streakDf['streak_category'] = np.select(conditions, values, default=None)

    return streakDf


def configBasketballStreakCats(streakDf):
    '''
    Adds basketball streak category to streaks dataframe based on streak name patterns

    Args:
        streakDf: dataframe of sofascore basketball streaks

    Returns:
        streakDf: dataframe of sofascore basketball streaks with streak category column
    '''

    streakDf['streak_name'] = streakDf['streak_name'].astype(str)

    conditions_basketball = [
        streakDf['streak_name'].str.contains('Game points'),
        streakDf['streak_name'].str.contains('Scored points'),
        streakDf['streak_name'].str.contains('First quarter'),
        streakDf['streak_name'].str.contains('First half'),
        streakDf['streak_name'].str.contains('wins|losses|Wins|Losses'),
    ]

    values_basketball = [
        'total_points',
        'total_points',
        'qtr_moneyline',
        'half_moneyline',
        'moneyline',
    ]

    streakDf['streak_category'] = np.select(conditions_basketball, values_basketball, default=None)

    return streakDf


def selectConfigStreakCats(sport, streakDf):
    '''
    Configures streak category columns based on the sport

    Args:
        sport: string of sport name
        streakDf: dataframe of sofascore streaks

    Returns:
        streakCatDf: dataframe of sofascore streaks with applicable sport streak category column 
    '''

    if sport == 'soccer':
        streakCatDf = configSoccerStreakCats(streakDf)

    if sport == 'basketball':
        streakCatDf = configBasketballStreakCats(streakDf)

    return streakCatDf


def sportOfferCategorySchemaDict():
    '''
    Dict to map a sport and its category to the corresponding dataframe schema functions

    Returns:
        schemaDict: dict for sport category schema mapping
    '''

    schemaDict = {
    "soccer": {
        #'events': {'schema': },
        'moneyline': {'schema': schemas.soccerMoneyline},
        'total_goals': {'schema': schemas.totalGoals},
        'btts': {'schema': schemas.btts},
        'first_score': {'schema': schemas.firstScore},
        'total_corners': {'schema': schemas.totalCorners},
        'total_cards': {'schema': schemas.totalCards},
        #'clean_sheet': {'schema': schemas.cleanSheet},
        'half_moneyline': {'schema': schemas.soccerHalfMoneyline},
    },
    # "hockey": {
    #     #events
    #     'moneyline': {'schema': },
    #     'total_goals': {'schema': },
    #     'period_btts': {'schema': },
    #     'period_moneyline': {'schema': },
    #     'period_total_goals': {'schema': },
    # },
    "basketball": {
        #'events': {'schema': },
        'moneyline': {'schema': schemas.basketballMoneyline},
        'total_points': {'schema': schemas.totalPoints},
        #'spread': {'schema': },
        'half_moneyline': {'schema': schemas.basketballHalfMoneyline},
        'qtr_moneyline': {'schema': schemas.qtrMoneyline},
    }
    #"football": {}
    #"baseball": {}
    }

    return schemaDict