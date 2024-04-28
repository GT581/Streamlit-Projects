from Pipelines.fantasypros import common
import pandas as pd
import time
import re


def renameDropRedZoneColumns(df, pos):
    if pos == 'qb':
        df.columns = [x[1] if x[1] not in df.columns[:x[0]] else f"{x[1]}_{list(df.columns[:x[0]]).count(x[1])}" for x in enumerate(df.columns)]
        columnsDrop = ['ATT_1', 'PCT_1', 'YDS_1', 'TD_1', 'ATT_2', 'YDS_2', 'TD_2', 'PCT_2']
        df = df.drop(columns=columnsDrop)
        df = df.rename(columns={'ATT': 'PASS ATT', 'PCT': 'PASS PCT', 'YDS': 'PASS YDS', 'TD': 'PASS TD',
        'ATT_3': 'RUSH ATT', 'YDS_3': 'RUSH YDS', 'TD_3': 'RUSH TD', 'PCT_3': 'RUSH PCT'})
        return df
    if pos == 'wr' or pos == 'te':
        df.columns = [x[1] if x[1] not in df.columns[:x[0]] else f"{x[1]}_{list(df.columns[:x[0]]).count(x[1])}" for x in enumerate(df.columns)]
        columnsDrop = ['YDS_1', 'TD_1', 'YDS_2', 'TD_2']
        df = df.drop(columns=columnsDrop)
        df = df.rename(columns={'YDS': 'REC YDS', 'TD': 'REC TD',
        'YDS_3': 'RUSH YDS', 'TD_3': 'RUSH TD', 'PCT': 'RUSH PCT', 'ATT': 'RUSH ATT'})
        return df
    if pos == 'rb':
        df.columns = [x[1] if x[1] not in df.columns[:x[0]] else f"{x[1]}_{list(df.columns[:x[0]]).count(x[1])}" for x in enumerate(df.columns)]
        columnsDrop = ['YDS_1', 'TD_1', 'YDS_2', 'TD_2']
        df = df.drop(columns=columnsDrop)
        df = df.rename(columns={'YDS': 'RUSH YDS', 'TD': 'RUSH TD', 
        'PCT': 'RUSH PCT', 'YDS_3': 'REC YDS', 'TD_3': 'REC TD'})
        return df


def convertRedZonePercentages(df, pos):
    if pos == 'qb':
        df['PASS PCT'] = round(df['PASS PCT'].str.replace('%', '').astype(float) / 100, 2) #apply(common.convertDecimal)
        df['RUSH PCT'] = round(df['RUSH PCT'].str.replace('%', '').astype(float) / 100, 2) #apply(common.convertDecimal)
        df['ROST %'] = round(df['ROST %'].str.replace('%', '').astype(float) / 100, 2) #apply(common.convertDecimal)
        return df
    if pos == 'wr' or pos == 'te':
        df['REC PCT'] = round(df['REC PCT'].str.replace('%', '').astype(float) / 100, 2) #.apply(common.convertDecimal)
        df['TGT PCT'] = round(df['TGT PCT'].str.replace('%', '').astype(float) / 100, 2) #.apply(common.convertDecimal)
        df['RUSH PCT'] = round(df['RUSH PCT'].str.replace('%', '').astype(float) / 100, 2) #.apply(common.convertDecimal)
        df['ROST %'] = round(df['ROST %'].str.replace('%', '').astype(float) / 100, 2) #.apply(common.convertDecimal)
        return df
    if pos == 'rb':
        df['RUSH PCT'] = round(df['RUSH PCT'].str.replace('%', '').astype(float) / 100, 2) #.apply(common.convertDecimal)
        df['REC PCT'] = round(df['REC PCT'].str.replace('%', '').astype(float) / 100, 2) #.apply(common.convertDecimal)
        df['TGT PCT'] = round(df['TGT PCT'].str.replace('%', '').astype(float) / 100, 2) #.apply(common.convertDecimal)
        df['ROST %'] = round(df['ROST %'].str.replace('%', '').astype(float) / 100, 2) #.apply(common.convertDecimal)
        return df


def createRedZoneCols(df, year, week, pos, yard):
    df['Team'] = df['Player'].apply(lambda x: common.stripTeam(x))
    df['Player'] = df['Player'].apply(lambda x: re.sub(r'\s*\([^)]*\)\s*', '', x))
    df['Year'] = year
    df['Week'] = week
    df['Position'] = pos.upper()
    df['Inside'] = yard
    colOrder = ['Year', 'Week', 'Position', 'Player', 'Team', 'Inside'] + [col for col in df.columns if col not in ['Year', 'Week', 'Position', 'Player', 'Team', 'Inside']]
    df = df[colOrder]
    return df


def getRedZoneWeekData(pos, years, weeks, yards):
    dfList = []

    for year in years:
        for week in weeks:
            for yard in yards:
                url = f'https://www.fantasypros.com/nfl/red-zone-stats/{pos}.php?year={year}&scoring=PPR&range=week&week={week}&yardline={yard}'
                df = common.scrapeFantasyProsTable(url)
                dfCols = createRedZoneCols(df, year, week, pos, yard)
                dfNamed = renameDropRedZoneColumns(dfCols, pos)
                dfP = convertRedZonePercentages(dfNamed, pos)
                dfList.append(dfP)
                time.sleep(5)

    dfAdv = pd.concat(dfList, ignore_index=True)
    dfAdv.to_csv(f'Pipelines/fantasypros/data/redzone/{pos.upper()}_RZ.csv')