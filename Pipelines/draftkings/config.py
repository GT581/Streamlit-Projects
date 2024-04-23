from Pipelines.draftkings.soccer import parse as dksp
from Pipelines.draftkings.basketball import parse as dkbp


def sportEventGroupIdDict():
    '''
    Mapping config dict for sports leagues and their draftkings event group IDs to use in API calls

    Returns:
        sportsEventGroupIdDict: dict for event group ID mapping
    '''

    sportsEventGroupIdDict = {
    "hockey": {
        "NHL": {"eventGroup": "42133"}
    },
    #"football": [{"eventGroup": "88808"}], #NFL
    "basketball": {
        "NBA": {"eventGroup": "42648"},
        "NCAAM": {"eventGroup": "92483"}
    },
    #"baseball": [{"eventGroup": "84240"}], #MLB
    "soccer": {
        "England - Premier League": {"eventGroup": "40253"},
        "Spain - La Liga": {"eventGroup": "40031"},
        "Italy - Serie A": {"eventGroup": "40030"},
        "Germany - Bundesliga": {"eventGroup": "40481"},
        "France - Ligue 1": {"eventGroup": "40032"},
        "Champions League": {"eventGroup": "40685"},
        "Europa League": {"eventGroup": "41410"},
        "USA - MLS": {"eventGroup": "89345"} 
    }
    }

    return sportsEventGroupIdDict


def sportOfferCategoryTableDict():
    '''
    Mapping config dict for each betting category for each sport, with parsing functions for access after draftkings API call

    Returns:
        sportOfferCategoryDict: dict for offer and sub category ID mapping with corresponding parsing functions
    '''

    sportOfferCategoryDict = {
    "soccer": {
        'events': {"offerCategoryId": 490, "subCategoryId": 4514, "parseFunction": dksp.parseDkSoccerEvents},  # Game Lines, Moneyline (events in all)
        'moneyline': {"offerCategoryId": 490, "subCategoryId": 4514, "parseFunction": dksp.parseDkSoccerMoneyline},  # Game Lines, Moneyline
        'total_goals': {"offerCategoryId": 490, "subCategoryId": 13171, "parseFunction": dksp.parseDkSoccerTotals},  # Game Lines, Total Goals
        'btts': {"offerCategoryId": 540, "subCategoryId": 5645, "parseFunction": dksp.parseDkSoccerBtts},  # Game Props, BTTS
        'first_score': {"offerCategoryId": 540, "subCategoryId": 6728, "parseFunction": dksp.parseDkSoccerFirstScore},  # Game Props, First / Last Goal
        'total_corners': {"offerCategoryId": 543, "subCategoryId": 4846, "parseFunction": dksp.parseDkSoccerTotals},  # Corners, Total Corners
        'total_cards': {"offerCategoryId": 647, "subCategoryId": 6828, "parseFunction": dksp.parseDkSoccerTotals},  # Cards, Total Bookings
        'clean_sheet': {"offerCategoryId": 541, "subCategoryId": 6842, "parseFunction": dksp.parseDkSoccerCleanSheet},  # Team Props, Clean Sheet
        'half_moneyline': {"offerCategoryId": 544, "subCategoryId": 11273, "parseFunction": dksp.parseDkSoccerHalfMoneyline}  # Halves, Moneyline
    },
    "hockey": {
        #events
        'moneyline': {"offerCategoryId": 496, "subCategoryId": 4525}, # Game Lines, Game, Moneyline
        'total_goals': {"offerCategoryId": 496, "subCategoryId": 4525}, # Game Lines, Game, Total Goals
        'period_btts': {"offerCategoryId": 548, "subCategoryId": 6271}, # Periods, 1st Period, BTTS
        'period_moneyline': {"offerCategoryId": 548, "subCategoryId": 4761}, # Periods, 1st Period, Moneyline
        'period_total_goals': {"offerCategoryId": 548, "subCategoryId": 4761}  # Periods, 1st Period, Total
    },
    "basketball": {
        'events': {"offerCategoryId": 487, "subCategoryId": 4511, "parseFunction": dkbp.parseDkBasketballEvents},  #Game Lines, Moneyline (events in all)
        'moneyline': {"offerCategoryId": 487, "subCategoryId": 4511, "parseFunction": dkbp.parseDkBasketballMoneyline},  # Game Lines, Game, Moneyline
        'total_points': {"offerCategoryId": 487, "subCategoryId": 4511, "parseFunction": dkbp.parseDkBasketballTotals},  # Game Lines, Game, Total Points
        'spread': {"offerCategoryId": 487, "subCategoryId": 4511, "parseFunction": dkbp.parseDkBasketballSpreads},  # Game Lines, Game, Spread
        'half_moneyline': {"offerCategoryId": 520, "subCategoryId": 4598, "parseFunction": dkbp.parseDkBasketballHalfMoneyline},  # Halves, 1stH
        'qtr_moneyline': {"offerCategoryId": 522, "subCategoryId": 4600, "parseFunction": dkbp.parseDkBasketballQtrMoneyline}  # Quarters, 1stQ
    }
    #"football": {}
    #"baseball": {}
    }

    return sportOfferCategoryDict