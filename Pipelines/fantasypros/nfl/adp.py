from fantasypros.common import scrapeFantasyProsTable, stripCreateFantasyProsPosition, renameFantasyProsColumns, fantasyProsUrls


def getAdpDf():
    urlDict = fantasyProsUrls()
    url = urlDict['adp']
    adpDf = scrapeFantasyProsTable(url)
    return adpDf


def transformAdpDf(adpDf):
    adpColumns = {
    'Rank': 'adp',
    'Player Team': 'player',
    'POS': 'position_rnk',
    'AVG': 'avg_adp'
    }
    adpDfRk = stripCreateFantasyProsPosition(adpDf)
    adpDfFinal = renameFantasyProsColumns(adpDfRk, adpColumns)
    return adpDfFinal