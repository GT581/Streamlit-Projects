import Pipelines.sports_common as sc
import json
import http.client
import pandas as pd
import Pipelines.sofascore.config as cf
#from sqlalchemy import create_engine, Integer, Text, DateTime, BOOLEAN, text


def getSofaEvents(sport, dateInput):
    '''
    Get request to retrieve event data for a given sport and date from the sofascore API

    Args: 
        sport: string of sport name
        dateInput: string of current date in YYYY-mm-dd format

    Returns: 
        eventsResponse: sofascore eventsResponse JSON
    '''

    sportUrl = cf.sportLeagueNameInputMapping(sport)

    site = 'api.sofascore.com'

    url = f"/api/v1/sport/{sportUrl}/scheduled-events/{dateInput}"

    conn = http.client.HTTPSConnection(site)

    payload = ''

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


def parseSofaEvents(eventsResponse, sport):
    '''
    Parse the sofascore API event JSON

    Args: 
        eventsResponse: eventsResponse JSON from getSofaEvents
        sport: string of sport name

    Returns: 
        matchesDf: Dataframe of sofascore event data
    '''

    leagueIdList = cf.sportLeagueIdMapping(sport)
    currentDTime = sc.getCurrentDTimeEst()

    matchSchema = ['sofa_match_id', 'league', 'season', 'home_team', 'away_team', 'sofa_home_team_id', 'sofa_away_team_id', 'match_dtime', 'db_ts']
    matchData = []

    #Iterate through each event dict in the events list
    for d in eventsResponse['events']:
        if 'uniqueTournament' in d['tournament']:
            if d['tournament']['uniqueTournament']['id'] in leagueIdList: #only parse and append data for configued / desired leagues
                league = d['tournament']['name']
                season = d['season']['name']
                homeSofaId = d['homeTeam']['id']
                homeTeam = d['homeTeam']['name']
                awaySofaId = d['awayTeam']['id']
                awayTeam = d['awayTeam']['name']
                matchId = d['id']
                startTimestamp = d['startTimestamp']
                estDtFormatted = sc.convertUnixEST(startTimestamp)
                matchData.append([matchId, league, season, homeTeam, awayTeam, homeSofaId, awaySofaId, estDtFormatted, currentDTime])
            else:
                continue

    matchesDf = pd.DataFrame(data=matchData, columns=matchSchema)

    return matchesDf


#Declare schema of parsed JSON data, append to stage events table, and execute CDC SQL to add or update main tables based on PK
# def writeSofaEvents(matchesDf, sport):
#     dbSchema = 'sofascore'
#     table = 'events'
#     schema = {
#         'sofa_match_id': Integer,
#         'sport_name': Text, 
#         'league': Text, 
#         'season': Text, 
#         'sofa_home_team_id': Integer, 
#         'home_team': Text, 
#         'sofa_away_team_id': Integer, 
#         'away_team': Text, 
#         'match_dtime': DateTime, 
#         'db_ts': DateTime
#         }
#     sc.writeStage(matchesDf, table, sport, dbSchema, schema)
#     sc.executeCdc(sport, dbSchema, table)
