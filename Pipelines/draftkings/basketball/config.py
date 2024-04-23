import draftkings.basketball.parse as dkbp
import draftkings.basketball.write as dkbw


def basketballEventGroupIds():
    basketballEventGroupIdDict = {
        "NBA": {"eventGroup": "42648"},
        "NCAAM": {"eventGroup": "92483"}
    }
    return basketballEventGroupIdDict


def basketballOfferCategoryIds():
    basketballOfferCategoryIdDict = {
        'events': {"offerCategoryId": 487, "subCategoryId": 4511, "parseFunction": dkbp.parseDkBasketballEvents, "writeFunction": dkbw.writeDkBasketballEvents}, #Game Lines, Moneyline (events in all)
        'moneyline': {"offerCategoryId": 487, "subCategoryId": 4511, "parseFunction": dkbp.parseDkBasketballMoneyline, "writeFunction": dkbw.writeDkBasketballMoneyline}, # Game Lines, Game, Moneyline
        'total_points': {"offerCategoryId": 487, "subCategoryId": 4511, "parseFunction": dkbp.parseDkBasketballTotals, "writeFunction": dkbw.writeDkBasketballTotals}, # Game Lines, Game, Total Points
        'spread': {"offerCategoryId": 487, "subCategoryId": 4511, "parseFunction": dkbp.parseDkBasketballSpreads, "writeFunction": dkbw.writeDkBasketballSpreads}, # Game Lines, Game, Spread
        'half_moneyline': {"offerCategoryId": 520, "subCategoryId": 4598, "parseFunction": dkbp.parseDkBasketballHalfMoneyline, "writeFunction": dkbw.writeDkBasketballHalfMoneyline}, # Halves, 1stH
        'qtr_moneyline': {"offerCategoryId": 522, "subCategoryId": 4600, "parseFunction": dkbp.parseDkBasketballQtrMoneyline, "writeFunction": dkbw.writeDkBasketballQtrMoneyline}  # Quarters, 1stQ
    }
    return basketballOfferCategoryIdDict