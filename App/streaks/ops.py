from Pipelines.sofascore import config as socon
import streamlit as st
from Pipelines import sports_common
from App.streaks import config, schemas
import pandas as pd
from datetime import datetime
import warnings


warnings.filterwarnings("ignore")


def loadSportSelection():
    '''
    Loads list of configured sports to select from

    Returns:
        sportsList: list of configured sports
    '''

    #sportsEventGroupIdDict = dkcon.sportEventGroupIdDict()
    #sportsList = list(sportsEventGroupIdDict.keys())

    sportsList = ['soccer', 'basketball']

    return sportsList


def filterDfDate(matchesDf, dateInput):
    '''
    Filters match dataframe for matches only on the selected date

    Args:
        matchesDf: dataframe of matches
        dateInput: string of selected date in YYYY-mm-dd format

    Returns:
        matchesFiltered: dataframe of filtered matches
    '''

    matchesDf['match_dtime'] = pd.to_datetime(matchesDf['match_dtime'])
    matchesDf['date_only'] = matchesDf['match_dtime'].dt.date

    matchesFiltered = matchesDf[matchesDf['date_only'] == dateInput]
    matchesFiltered = matchesFiltered.drop(columns=['date_only'])

    return matchesFiltered


def loadDkSofaTeamMapping(sport):
    '''
    Loads the CSV file for mapping sofascore teams to draftkings teams for a sport

    Args:
        sport: string of sport name

    Returns:
        mapDf: dataframe of the mapping file for a given sport
    '''

    mapDf = pd.read_csv(f'App/streaks/mapping/{sport}_mapping.csv')
    mapDf['dk_team_id'] = mapDf['dk_team_id'].fillna(0).astype(int)
    mapDf['sofa_team_id'] = mapDf['sofa_team_id'].fillna(0).astype(int)
    mapDf['dk_team'] = mapDf['dk_team'].fillna(0)
    mapDf['sofa_team'] = mapDf['sofa_team'].fillna(0)

    return mapDf


def loadSofaTeamNameMapping(sport, leagueDf):
    '''
    Maps sofascore team names to common team names in the mapping file

    Args:
        sport: string of sport name
        leagueDf: dataframe of matches for a selected league

    Returns:
        df: dataframe of matches for a selected league with mapped team names
    '''

    mapDf = pd.read_csv(f'App/streaks/mapping/{sport}_mapping.csv')
    df = pd.merge(leagueDf, mapDf, left_on='sofa_home_team_id', right_on='sofa_team_id', how='inner')
    df2 = pd.merge(df, mapDf, left_on='sofa_away_team_id', right_on='sofa_team_id', how='inner')
    df3 = df2[['sofa_match_id', 'league', 'season', 'team_x', 'team_y', 'match_dtime']]
    df4 = df3.rename(columns={'team_x': 'home_team', 'team_y': 'away_team'})

    return df4.drop_duplicates()


def dkSofaEventMatching(mapDf, matchesDf, eventsDf, dateInput):
    '''
    Join match data from sofascore and draftkings on each corresponding team IDs 
    and filter for matches on selected date

    Args:
        mapDf: dataframe of the mapping file for a given sport
        matchesDf: dataframe of draftkings matches
        eventsDf: dataframe of sofascore events
        dateInput: string of selected date in YYYY-mm-dd format

    Returns:
        df: dataframe of matched sofascore and draftkings events
    '''

    df = pd.merge(matchesDf, mapDf, left_on='sofa_home_team_id', right_on='sofa_team_id', how='inner')
    df2 = pd.merge(df, mapDf, left_on='sofa_away_team_id', right_on='sofa_team_id', how='inner')
    df3 = pd.merge(eventsDf, df2, left_on='dk_home_team_id', right_on='dk_team_id_x', how='inner')
    df4 = pd.merge(eventsDf, df3, left_on='dk_away_team_id', right_on='dk_team_id_y', how='inner')

    df4['home_team_x'] = df4['team_x']
    df4['away_team_x'] = df4['team_y']
    df5 = df4[['sofa_match_id',	'dk_match_id_x', 'league_x','home_team_x',	'away_team_x',	'match_dtime_y']]
    df5.columns = df5.columns.str.replace('_x', '').str.replace('_y', '')

    df6 = filterDfDate(df5, dateInput)

    if df6.empty:
        st.error(f'No bet data available to match to streaks. The match either already took place, or odds are not out yet.')
        st.stop()
    
    return df6


def loadTeamMatchups(eventMatchDf):
    '''
    Loads list of matchups for selection

    Args:
        eventMatchDf: dataframe of matched events

    Returns:
        matches: list of matchups
    '''

    matches = eventMatchDf.apply(lambda x: f"{x['home_team']} vs. {x['away_team']}", axis=1).unique()

    return matches


def loadMatchIds(match, eventMatchDf):
    '''
    Loads the sofascore and draftkings event IDs for selected match

    Args:
        match: selected match
        eventMatchDf: dataframe of matched events
    
    Returns:
        sofaMatchId: sofascore match ID
        dkMatchId: draftkings match ID
    '''

    home_team, away_team = match.split(' vs. ')
    matchRow = eventMatchDf[(eventMatchDf['home_team'] == home_team) & (eventMatchDf['away_team'] == away_team)]
    matchDict = socon.createMatchesDfDict(matchRow)

    if matchDict:
        sofaMatchId = matchDict[0]['sofa_match_id']
        dkMatchId = matchDict[0]['dk_match_id']
    else:
        st.error(f'No bet data available to match to streaks. The match either already took place, or odds are not out yet.')
        st.stop()
    
    return sofaMatchId, dkMatchId


def checkPastDate(dt):
    '''
    Checks if selected date is in the past

    Args:
        dt: string selected date
    '''

    currentDt = sports_common.genFormattedDate()
    currentDtFormat = datetime.strptime(currentDt, "%Y-%m-%d").date()

    if dt < currentDtFormat:
        st.error('You have selected a past date. Date will need to be today or later to pull any available odds.')
        st.stop()
    else:
        pass


def sofaStreaksDkOddsMatching(eventMatchDf, catMatchDf, streakCatDf, category, sport):
    '''
    Matches draftkings odds to sofascore streaks to display final screener results

    Args:
        eventMatchDf: dataframe of matched events
        catMatchDf: dataframe of draftkings category odds for a given match
        streakCatDf: dataframe of sofascore streaks with applicable sport streak category column 
        category: string of bet category
        sport: string of sport name

    Returns:
        finalDf: dataframe of match streaks and their corresponding odds
    '''

    finalDf = pd.merge(eventMatchDf, streakCatDf, left_on='sofa_match_id', right_on='sofa_match_id', how='inner')
    finalDf2 = pd.merge(finalDf, catMatchDf, left_on='dk_match_id', right_on='dk_match_id', how='inner')
    
    finalDf3 = finalDf2[finalDf2['streak_category'] == category]

    sofaSchema, sofaTotalSchema, sofaDisplaySchema = schemas.sofaColumnsCommon()

    schemaDict = config.sportOfferCategorySchemaDict()
    schemaFunc = schemaDict[sport][category]['schema']
    schema, displaySchema = schemaFunc()

    if 'total_' in category or 'btts' in category:
        sofaSchema = sofaTotalSchema

    sofaSchema.extend(schema)

    finalDf4 = finalDf3[sofaSchema]
    finalDf4.columns = finalDf4.columns.str.replace('_x', '')

    sofaDisplaySchema.extend(displaySchema)
    finalDf4.columns = sofaDisplaySchema

    finalDf5 = finalDf4.drop_duplicates()

    if finalDf5.empty:
        st.error(f'No bet data is available yet to match to streaks')
        st.stop()

    return finalDf5