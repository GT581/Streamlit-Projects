from fantasypros.common import scrapeFantasyProsTable, stripCreateFantasyProsPosition, renameFantasyProsColumns, fantasyProsUrls


def getFlexDf():
    urlDict = fantasyProsUrls()
    url = urlDict['flexProj']
    flexDf = scrapeFantasyProsTable(url)
    return flexDf


def getQbDf():
    urlDict = fantasyProsUrls()
    url = urlDict['qbProj']
    qbDf = scrapeFantasyProsTable(url)
    return qbDf


def transformFlexDf(flexDf):
    flexProjColumns = {
    'Player': 'player',
    'POS': 'position_rnk',
    'ATT': 'rush_att',
    'YDS': 'rush_yds',
    'TDS': 'rush_tds',
    'REC': 'receptions',
    'YDS.1': 'rec_yds',
    'TDS.1': 'rec_tds',
    'FL': 'fumbles',
    'FPTS': 'total_points'
    }
    flexDfRk = stripCreateFantasyProsPosition(flexDf)
    flexDfFinal = renameFantasyProsColumns(flexDfRk, flexProjColumns)
    return flexDfFinal


def transformQbDf(qbDf):
    qbProjColumns = {
    'Player': 'player',
    'ATT': 'pass_att',
    'CMP': 'pass_cmp',
    'YDS': 'pass_yds',
    'TDS': 'pass_tds',
    'INTS': 'interceptions',
    'ATT.1': 'rush_att',
    'YDS.1': 'rush_yds',
    'TDS.1': 'rush_tds',
    'FL': 'fumbles',
    'FPTS': 'total_points'
    }
    qbDf.insert(qbDf.columns.get_loc('Player') + 1, 'position', 'QB')
    qbDf.insert(qbDf.columns.get_loc('position') + 1, 'position_rnk', 'QB' + (qbDf.index + 1).astype(str))
    qbDfFinal = renameFantasyProsColumns(qbDf, qbProjColumns)
    return qbDfFinal