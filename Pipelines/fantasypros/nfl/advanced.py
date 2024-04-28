from Pipelines.fantasypros import common
import pandas as pd
import time
import re


def convertAdvPercentages(df, pos):
    if pos == 'qb':
        df['PCT'] = df['PCT'].apply(common.convertDecimal)
        return df
    if pos == 'wr' or pos == 'te':
        df['% TM'] = df['% TM'].apply(common.convertDecimal)
        return df
    else:
        return df


def createAdvCols(df, year, week, pos):
    df['Team'] = df['Player'].apply(lambda x: common.stripTeam(x))
    df['Player'] = df['Player'].apply(lambda x: re.sub(r'\s*\([^)]*\)\s*', '', x))
    df['Year'] = year
    df['Week'] = week
    df['Position'] = pos.upper()
    colOrder = ['Year', 'Week', 'Position', 'Player', 'Team'] + [col for col in df.columns if col not in ['Year', 'Week', 'Position', 'Player', 'Team']]
    df = df[colOrder]
    return df


def getAdvWeekData(pos, years, weeks):
    dfList = []

    for year in years:
        for week in weeks:
            url = f'https://www.fantasypros.com/nfl/advanced-stats-{pos}.php?year={year}&week={week}&range=week'
            df = common.scrapeFantasyProsTable(url)
            dfCols = createAdvCols(df, year, week, pos)
            dfP = convertAdvPercentages(dfCols, pos)
            dfList.append(dfP)
            time.sleep(5)

    dfAdv = pd.concat(dfList, ignore_index=True)
    dfAdv.to_csv(f'Pipelines/fantasypros/data/advanced/{pos.upper()}.csv')