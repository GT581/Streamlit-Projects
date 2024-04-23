import http.client
import json
import pandas as pd
import Pipelines.sofascore.config as cf
import Pipelines.sports_common as sc
#from sqlalchemy import create_engine, Integer, Text, DateTime, BOOLEAN, text


def getSofaStreaks(matchId):
    '''
    Get request to retrieve streak data for a given match from the sofascore API

    Args: 
        matchId: sofascore matchId

    Returns: 
        streaksResponse: sofascore streaksResponse JSON
    '''

    site = 'api.sofascore.com'

    url = f"/api/v1/event/{matchId}/team-streaks"

    conn = http.client.HTTPSConnection(site)

    payload = ''

    #Use headers as viewing in web browser
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'origin': 'https://www.sofascore.com',
    'priority': 'u=1, i',
    'referer': 'https://www.sofascore.com/',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    conn.request("GET", url, payload, headers)

    response = conn.getresponse()

    data = response.read()

    eventsResponse = json.loads(data)

    conn.close()

    return eventsResponse


#Parse the streaks JSON and create a dataframe. Add boolean flag for if team or H2H streak.
def parseSofaStreaks(streaksResponse, matchId, matchesDict):
    '''
    Parse the sofascore API match streaks JSON

    Args: 
        streaksResponse: streaksResponse JSON from getSofaStreaks
        matchId: sofascore matchId
        matchesDict: dictionary for the matchId row from sofascore match data

    Returns: 
        streakDf: Dataframe of sofascore event data
    '''

    currentDTime = sc.getCurrentDTimeEst()

    #Extract match metadata from dict that is not available in streak data
    league = matchesDict['league']
    homeTeam = matchesDict['home_team']
    awayTeam = matchesDict['away_team']

    streakSchema = ['sofa_match_id', 'league', 'streak_name', 'streak_value', 'streak_label', 'hth_ind', 'continued_ind', 'db_ts']
    streakList = []

    #Parse team only streaks
    for d in streaksResponse['general']:
        streakName = d['name']
        streakValue = d['value']
        streakLabel = d['team']
        if streakLabel == 'home':
            streakLabel = homeTeam
        if streakLabel == 'away':
            streakLabel = awayTeam
        if streakLabel == 'both':
            streakLabel = f'{homeTeam} | {awayTeam}'
        hthFlag = False
        continuedFlag = d.get('continued', None)
        streakList.append([matchId, league, streakName, streakValue, streakLabel, hthFlag, continuedFlag, currentDTime])
    
    #Parse streaks specific to the matchup
    for d in streaksResponse['head2head']:
        h2hStreakName = d['name']
        h2hStreakValue = d['value']
        h2hStreakLabel = d['team']
        if h2hStreakLabel == 'home':
            h2hStreakLabel = homeTeam
        if h2hStreakLabel == 'away':
            h2hStreakLabel = awayTeam
        if h2hStreakLabel == 'both':
            h2hStreakLabel = f'{homeTeam} | {awayTeam}'
        hthFlag = True
        continuedFlag = d.get('continued', None)
        streakList.append([matchId, league, h2hStreakName, h2hStreakValue, h2hStreakLabel, hthFlag, continuedFlag, currentDTime])
    
    streakDf = pd.DataFrame(data=streakList, columns=streakSchema)

    return streakDf


#Declare schema of parsed JSON data, append to stage streaks table, and execute CDC SQL to add or update main tables based on PK
# def writeSofaStreaks(streakDf, sport):
#     dbSchema = 'sofascore'
#     table = 'streaks'
#     schema = {
#         'sofa_match_id': Integer,
#         'sport_name': Text, 
#         'streak_name': Text, 
#         'streak_value': Text, 
#         'streak_label': Text,
#         'hth_ind': BOOLEAN,
#         'continued_ind': BOOLEAN,
#         'db_ts': DateTime
#         }
#     sc.writeStage(streakDf, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)