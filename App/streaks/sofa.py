import streamlit as st
from Pipelines.sofascore import events, config as socon, streaks
from Pipelines import sports_common
from datetime import datetime
from App.streaks import ops, schemas


def getSofaDateSportEvents(sport, dateInput):
    '''
    Get and parse sofascore event data for selected date

    Args:
        sport: string of sport name
        dateInput: string of selected date YYYY-mm-dd

    Returns:
        matchesDf: dataframe of matches 
    '''

    eventsResponse = events.getSofaEvents(sport, dateInput)
    if 'error' in eventsResponse.keys():
        st.error(f'Sofascore response returned error: {eventsResponse}')
        st.stop()
    
    matches = events.parseSofaEvents(eventsResponse, sport)
    if matches.empty:
        st.error(f'No matches available for {sport} in the top leagues on {dateInput}')
        st.stop()
    
    matchesDf = ops.filterDfDate(matches, dateInput)

    return matchesDf


#also for league matches
def displayMatchesDf(matchesDf):
    '''
    Filter and rename columns to display matches

    Args:
        matchesDf: dataframe of matches

    Returns:
        matchesDfDisplay: dataframe of matches for display
    '''

    schema, displaySchema = schemas.sofaMatches()
    matchesDfDisplay = matchesDf[schema]
    matchesDfDisplay.columns = displaySchema

    return matchesDfDisplay


def loadSofaDateSportEventLeagues(matchesDf):
    '''
    Load all leagues of the matches for selection

    Args:
        matchesDf: dataframe of matches

    Returns:
        leagues: list of leagues for matches
    '''

    leagues = matchesDf['league'].unique()

    return leagues


def loadSofaDateSportEventLeagueMatches(league, matchesDf):
    '''
    Load all matches for the selected league

    Args:
        league: string of selected league
        matchesDf: dataframe of matches
    
    Returns:
        leagueDf: dataframe of matches filtered by selected league
    '''

    leagueDf = matchesDf[matchesDf['league'] == league]

    return leagueDf


def checkSofaMatchId(match, matchesDf):
    '''
    Checks if a match has already taken place

    Args:
        match: string of selected match
        matchesDf: dataframe of matches

    Returns:
        sofaMatchId: string of sofascore match ID
        bool: True if past date, False if not
    '''

    home_team, away_team = match.split(' vs. ')
    matchRow = matchesDf[(matchesDf['home_team'] == home_team) & (matchesDf['away_team'] == away_team)]
    matchDict = socon.createMatchesDfDict(matchRow)

    sofaMatchId = matchDict[0]['sofa_match_id']
    matchTime = matchDict[0]['match_dtime']

    currentDatetime = sports_common.getCurrentDTimeEst()
    currentDatetime = datetime.strptime(currentDatetime, '%Y-%m-%d %H:%M:%S')

    if matchTime < currentDatetime:
        past = True
    else:
        past = False

    return sofaMatchId, past


def getSofaMatchStreaks(sofaMatchId, leagueNamedDf):
    '''
    Get and parse sofascore streaks data for a match

    Args:
        sofaMatchId: string of sofascore match ID
        leagueNamedDf: dataframe of matches for a league with mapped names

    Returns:
        streakDf: dataframe of sofascore streaks data
    '''

    matchIdDictList = socon.createMatchesDfDict(leagueNamedDf)
    for matchesDict in matchIdDictList:
        matchId = matchesDict['sofa_match_id']
        if matchId == sofaMatchId:
            streaksResponse = streaks.getSofaStreaks(matchId)
            streakDf = streaks.parseSofaStreaks(streaksResponse, matchId, matchesDict)

    return streakDf


def displayStreakCatDf(streakCatDf):
    '''
    Filter and rename columns to display streaks data

    Args:
        streakCatDf: dataframe of sofascore streaks with applicable sport streak category column

    Returns:
        streakCatDfDisplay: dataframe of sofascore streaks with applicable sport streak category columns for display
    '''

    schema, displaySchema = schemas.sofaStreaks()
    streakCatDfDisplay = streakCatDf[schema]
    streakCatDfDisplay.columns = displaySchema
    streakCatDfDisplay = streakCatDfDisplay[streakCatDfDisplay['Streak Category'].notna()]

    return streakCatDfDisplay


def loadMatchStreakCats(streakCatDf):
    '''
    Load available streak categories for a match

    Args:
        streakCatDf: dataframe of sofascore streaks with applicable sport streak category column

    Returns:
        filteredCategories: list of available streak categories
    '''

    categories = streakCatDf['streak_category'].unique()
    filteredCategories = list(filter(lambda x: x is not None, categories))

    return filteredCategories