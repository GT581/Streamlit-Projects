import requests 
import pandas as pd
from datetime import datetime


def getYahooAdp(resultSize):
    '''
    Get request to retrieve Yahoo Fantasy Football ADP data

    Args: 
        resultSize: number of players to return from Yahoo request

    Returns: 
        yahooResponse: yahooResponse JSON
    '''

    #resultSize is added to the url
    url = f"https://pub-api-ro.fantasysports.yahoo.com/fantasy/v2/league/449.l.public;out=settings/players;position=ALL;start=0;count={resultSize};sort=rank_season;search=;out=auction_values,ranks;ranks=season;ranks_by_position=season;out=expert_ranks;expert_ranks.rank_type=projected_season_remaining/draft_analysis;cut_types=diamond;slices=last7days?format=json_f"

    payload = {}

    #Use headers as viewing in web browser
    headers = {
      'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
      'Referer': 'https://football.fantasysports.yahoo.com/',
      'sec-ch-ua-mobile': '?0',
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
      'sec-ch-ua-platform': '"macOS"'
    }

    yahooResponse = requests.request("GET", url, headers=headers, data=payload).json()

    return yahooResponse


def parseYahooAdp(yahooResponse):
    '''
    Parse Yahoo Fantasy Football ADP data JSON

    Args: 
        yahooResponse: yahooResponse JSON from getYahooADP

    Returns: 
        playersDf: Dataframe of Yahoo ADP data
    '''

    playerSchema = ['yahoo_rank', 'yahoo_adp', 'player', 'team', 'position']
    playerList = []

    #Iterate through each player dict in the players list
    for d in yahooResponse['fantasy_content']['league']['players']:
        player = d['player']['name']['full']
        position = d['player']['display_position']
        team = d['player']['editorial_team_abbr']
        teamUpper = team.upper() #covert team abbreviations to CAPS to be consistent with other sites
        adp = d['player']['draft_analysis']['average_pick']

        for r in d['player']['player_ranks']:
            currentYear = datetime.now().strftime('%Y') #only grab current year's data
            if r['player_rank']['rank_season'] == currentYear and 'rank_position' not in r['player_rank']: #ignore position rankings
                rank = r['player_rank']['rank_value']
            else:
                continue
        
        playerList.append([rank, adp, player, teamUpper, position])

    playersDf = pd.DataFrame(data=playerList, columns=playerSchema)

    return playersDf