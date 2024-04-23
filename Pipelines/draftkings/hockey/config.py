import draftkings.hockey.parse as dkhp
import draftkings.hockey.write as dkhw


def hockeyEventGroupIds():
    hockeyEventGroupIdDict = {
        "NHL": {"eventGroup": "42133"}
    }
    return hockeyEventGroupIdDict


def hockeyOfferCategoryIds():
    hockeyOfferCategoryIdDict = {
        #events
        'moneyline': {"offerCategoryId": 496, "subCategoryId": 4525}, # Game Lines, Game, Moneyline
        'total_goals': {"offerCategoryId": 496, "subCategoryId": 4525}, # Game Lines, Game, Total Goals
        'period_btts': {"offerCategoryId": 548, "subCategoryId": 6271}, # Periods, 1st Period, BTTS
        'period_moneyline': {"offerCategoryId": 548, "subCategoryId": 4761}, # Periods, 1st Period, Moneyline
        'period_total_goals': {"offerCategoryId": 548, "subCategoryId": 4761}  # Periods, 1st Period, Total
    }
    return hockeyOfferCategoryIdDict