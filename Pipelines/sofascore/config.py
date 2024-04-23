

#Change to dict with names*
def sportLeagueIdMapping(sport):
    '''
    Load list of sofascore league IDs for each sport to filter scheduled events for when calling the sofascore API

    Args: 
        sport: string of the sport name

    Returns: 
        leagueIdList: list of league IDs configured for the sport
    '''

    sportLeagueIdMappingDict = {
        'soccer': [17, 8, 23, 35, 34, 242, 7, 679],  # premier league, la liga, serie a, bundesliga, ligue 1, MLS, champions league, europa league, conference league: 17015
        'hockey': [234],  # NHL
        'basketball': [132, 648, 13434]  # NBA, NCAAM, NCAAM - March Madness
        #'american-football': [9464, 19510]  #NFL, NCAAF
    }

    leagueIdList = sportLeagueIdMappingDict[sport]

    return leagueIdList


def sportLeagueNameInputMapping(sport):
    '''
    Maps the more common / input sport name to the sofascore sport name for use in the API (ex: hockey > ice-hockey)

    Args: 
        sport: string of common / input sport name

    Returns: 
        sportInput: string of sofascore sport name
    '''

    sportLeagueNameInputMappingDict = {
        'soccer': 'football',
        'hockey': 'ice-hockey',
        'basketball': 'basketball'
        #'football': 'american-football'
    }

    sportInput = sportLeagueNameInputMappingDict[sport]

    return sportInput


def createMatchesDfDict(matchesDf):
    '''
    Create list of dicts of sofascore event dataframe representing each row to access in team streaks parsing

    Args: 
        matchesDf: dataframe from parseSofaEvents

    Returns: 
        matchIdDictList: list of dicts of sofascore event data
    '''

    matchIdDictList = matchesDf.to_dict(orient='records')

    return matchIdDictList