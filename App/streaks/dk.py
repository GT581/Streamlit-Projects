import streamlit as st
from Pipelines.draftkings import config as dkcon, common as dkcom


def getDkEvents(sport, dkLeague):
    '''
    Sends get request for draftkings event data and parses into a dataframe

    Args:
        sport: string of sport name
        dkLeague: string of draftkings league name
    
    Returns:
        eventsDf: dataframe of draftkings events for a given sport
        eventGroup: string of eventGroup ID for draftkings league
    '''

    sportsLeagueEventGroupIdDict = dkcon.sportEventGroupIdDict()
    sportOfferCategoryDict = dkcon.sportOfferCategoryTableDict()

    eventGroup = sportsLeagueEventGroupIdDict[sport][dkLeague]['eventGroup']
    offerCategoryId = sportOfferCategoryDict[sport]['events']['offerCategoryId']
    subCategoryId = sportOfferCategoryDict[sport]['events']['subCategoryId']

    dkResponse = dkcom.getDkData(eventGroup, offerCategoryId, subCategoryId)
    if 'errorStatus' in dkResponse.keys():
        errorStatus = dkResponse['errorStatus']
        st.error('No bet data available to match to streaks. The match either already took place, or odds are not out yet.')
        print(f'DK response returned error for {sport} league {dkLeague}: {errorStatus}')
        st.stop()

    parseFunction = sportOfferCategoryDict[sport]['events']['parseFunction']
    eventsDf = parseFunction(dkResponse)

    return eventsDf, eventGroup


def getDkCatOdds(category, sport, eventGroup, dkMatchId):
    '''
    Sends get response for draftkings odds for a given sport / league / category / match

    Args:
        category: string of sport bet category
        sport: string of sport name
        eventGroup: string of draftkings event group / league ID
        dkMatchId: string of the draftkings ID for a match

    Returns:
        catMatchDf: dataframe of draftkings category odds for a given match
    '''

    sportOfferCategoryDict = dkcon.sportOfferCategoryTableDict()
    offerCategoryId = sportOfferCategoryDict[sport][category]['offerCategoryId']
    subCategoryId = sportOfferCategoryDict[sport][category]['subCategoryId']
    parseFunction = sportOfferCategoryDict[sport][category]['parseFunction']

    dkResponse = dkcom.getDkData(eventGroup, offerCategoryId, subCategoryId)
    if 'errorStatus' in dkResponse.keys():
        errorStatus = dkResponse['errorStatus']
        st.error('No bet data available to match to streaks. The match either already took place, or odds are not out yet.')
        print(f'DK response returned error for {category}: {errorStatus}')
        st.stop()
    else:
        if 'total_' in category:
            catDf = parseFunction(dkResponse, category)
        else:
            catDf = parseFunction(dkResponse)
        catMatchDf = catDf[catDf['dk_match_id'] == dkMatchId]

    return catMatchDf