import streamlit as st
from App.streaks import config, ops, dk, sofa


def selectDate():

    #Date selection for pulling from Sofascore
    selected_date = st.date_input(
    'Select a Date:',
    )
    ops.checkPastDate(selected_date)

    return selected_date


def selectSport():

    #Sport selection options from configured sports
    sportsList = ops.loadSportSelection()

    selected_sport = st.selectbox(
        'Select a Sport:',
        sportsList,
        index = None,
        key = 'sport'
    )

    if selected_sport is None:
        st.stop()

    return selected_sport


def displayMatches(selected_sport, selected_date):

    #Dataframe of matches for date / sport. If error or empty df, will stop
    matchesDf = sofa.getSofaDateSportEvents(selected_sport, selected_date)
    matchesDfDisplay = sofa.displayMatchesDf(matchesDf)

    with st.expander('See All Matches for Selected Date'):
        st.dataframe(matchesDfDisplay, use_container_width = True, hide_index = True)
    
    return matchesDf


def selectLeague(matchesDf):

    #List of leagues to choose from for matches on the choosen date for the given sport
    leagueList = sofa.loadSofaDateSportEventLeagues(matchesDf)

    #User selects league
    selected_league = st.selectbox(
        'Select a League:',
        leagueList,
        index = None,
        key = 'league'
    )

    if selected_league is None:
        st.stop()
    
    return selected_league


def displayLeagueMatches(selected_league, selected_sport, matchesDf):

    #Filter sofascore events df for chosen league
    leagueDf = sofa.loadSofaDateSportEventLeagueMatches(selected_league, matchesDf)

    #Map sofascore team names to mapping common team names
    leagueNamedDf = ops.loadSofaTeamNameMapping(selected_sport, leagueDf)
    leagueNamedDfDisplay = sofa.displayMatchesDf(leagueNamedDf)

    with st.expander('See All Matches for Selected League'):
        st.dataframe(leagueNamedDfDisplay, use_container_width = True, hide_index = True)
    
    return leagueNamedDf


def selectMatch(leagueNamedDf):

    #Generate 'Home vs. Away' strings for match selection
    matches = ops.loadTeamMatchups(leagueNamedDf)

    #User chooses match
    selected_match = st.selectbox(
        'Select a Match:',
        matches,
        index = None,
        key = 'match'
    )

    if selected_match is None:
        st.stop()
    
    return selected_match


def matchEvents(selected_date, selected_sport, selected_league, selected_match, matchesDf):

    #Load DK league name equivalent
    dkLeague = config.dkSofaLeagueMapping(selected_sport, selected_league)

    #Dataframe of DK matches for sport / league and the league DK eventGroup number
    eventsDf, eventGroup = dk.getDkEvents(selected_sport, dkLeague)

    #Load sport mapping csv
    mapDf = ops.loadDkSofaTeamMapping(selected_sport)

    #Match DK events to Sofascore events
    eventMatchDf = ops.dkSofaEventMatching(mapDf, matchesDf, eventsDf, selected_date)

    #Parse out Sofascore and DK matchID from joined df
    sofaMatchId, dkMatchId = ops.loadMatchIds(selected_match, eventMatchDf)

    return sofaMatchId, dkMatchId, eventGroup, eventMatchDf


def displayStreaks(selected_sport, sofaMatchId, matchesDf):

    #Get dataframe of streaks for selected match
    streakDf = sofa.getSofaMatchStreaks(sofaMatchId, matchesDf)

    #Assign betting categories to streaks
    streakCatDf = config.selectConfigStreakCats(selected_sport, streakDf)
    streakCatDfDisplay = sofa.displayStreakCatDf(streakCatDf)

    with st.expander('See All Streaks for Selected Match:'):
        st.dataframe(streakCatDfDisplay, use_container_width = True, hide_index = True)
    
    return streakCatDf


def selectStreaks(streakCatDf):

    #List of streak categories available for the match
    categories = sofa.loadMatchStreakCats(streakCatDf)

    #User selects category
    selected_streak = st.selectbox(
        'Select a Streak Category to pull the odds for:',
        categories,
        index = None,
        key = 'streak'
    )

    if selected_streak is None:
        st.stop()
    
    return selected_streak


def displayOdds(selected_streak, selected_sport, eventGroup, dkMatchId, eventMatchDf, streakCatDf):

    #Get dataframe of odds for the selected sport / match / streak
    catMatchDf = dk.getDkCatOdds(selected_streak, selected_sport, eventGroup, dkMatchId)

    #Get final dataframe of joined data
    finalDf = ops.sofaStreaksDkOddsMatching(eventMatchDf, catMatchDf, streakCatDf, selected_streak, selected_sport)

    #Display final dataframe of joined data (Work on sizing, graphs?)
    st.dataframe(finalDf, use_container_width = True, hide_index = True)


def sportsStreaksOdds():
    
    selected_date = selectDate()
    selected_sport = selectSport()

    matchesDf = displayMatches(selected_sport, selected_date)

    selected_league = selectLeague(matchesDf)
    leagueNamedDf = displayLeagueMatches(selected_league, selected_sport, matchesDf)

    selected_match = selectMatch(leagueNamedDf)
    sofaMatchId, dkMatchId, eventGroup, eventMatchDf = matchEvents(selected_date, selected_sport, selected_league, selected_match, matchesDf)

    streakCatDf = displayStreaks(selected_sport, sofaMatchId, matchesDf)
    selected_streak = selectStreaks(streakCatDf)

    displayOdds(selected_streak, selected_sport, eventGroup, dkMatchId, eventMatchDf, streakCatDf)