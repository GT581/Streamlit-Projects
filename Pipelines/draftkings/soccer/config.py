import draftkings.soccer.parse as dksp
import draftkings.soccer.write as dksw


def soccerEventGroupIds():
    soccerEventGroupIdDict = {
        "England - Premier League": {"eventGroup": "40253"},
        "Spain - La Liga": {"eventGroup": "40031"},
        "Italy - Serie A": {"eventGroup": "40030"},
        "Germany - Bundesliga": {"eventGroup": "40481"},
        "France - Ligue 1": {"eventGroup": "40032"},
        "Champions League": {"eventGroup": "40685"},
        "Europa League": {"eventGroup": "41410"},
        "USA - MLS": {"eventGroup": "89345"}
    }
    return soccerEventGroupIdDict


def soccerOfferCategoryIds():
    soccerOfferCategoryIdDict = {
        'events': {"offerCategoryId": 490, "subCategoryId": 4514, "parseFunction": dksp.parseDkSoccerEvents, "writeFunction": dksw.writeDkSoccerEvents}, #Game Lines, Moneyline (events in all)
        'moneyline': {"offerCategoryId": 490, "subCategoryId": 4514, "parseFunction": dksp.parseDkSoccerMoneyline, "writeFunction": dksw.writeDkSoccerMoneyline},  # Game Lines, Moneyline
        'total_goals': {"offerCategoryId": 490, "subCategoryId": 13171, "parseFunction": dksp.parseDkSoccerTotals, "writeFunction": dksw.writeDkSoccerTotals}, # Game Lines, Total Goals
        'btts': {"offerCategoryId": 540, "subCategoryId": 5645, "parseFunction": dksp.parseDkSoccerBtts, "writeFunction": dksw.writeDkSoccerBtts},  #Game Props, BTTS
        'first_score': {"offerCategoryId": 540, "subCategoryId": 6728, "parseFunction": dksp.parseDkSoccerFirstScore, "writeFunction": dksw.writeDkSoccerFirstScore},  #Game Props, First / Last Goal
        'total_corners': {"offerCategoryId": 543, "subCategoryId": 4846, "parseFunction": dksp.parseDkSoccerTotals, "writeFunction": dksw.writeDkSoccerTotals},  #Corners, Total Corners
        'total_cards': {"offerCategoryId": 647, "subCategoryId": 6828, "parseFunction": dksp.parseDkSoccerTotals, "writeFunction": dksw.writeDkSoccerTotals},  #Cards, Total Bookings
        'clean_sheet': {"offerCategoryId": 541, "subCategoryId": 6842, "parseFunction": dksp.parseDkSoccerCleanSheet, "writeFunction": dksw.writeDkSoccerCleanSheet},  #Team Props, Clean Sheet
        'half_moneyline': {"offerCategoryId": 544, "subCategoryId": 11273, "parseFunction": dksp.parseDkSoccerHalfMoneyline, "writeFunction": dksw.writeDkSoccerHalfMoneyline} #Halves, Moneyline
    }
    return soccerOfferCategoryIdDict