import Pipelines.sports_common as sc
import Pipelines.draftkings.common as dk
import pandas as pd


def parseDkSoccerEvents(dkResponse):
    '''
    Parse the soccer event data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from soccer events offer category dict ID values

    Returns:
        dfEvents: draftkings soccer event dataframe
    '''

    eventSchema = ['dk_match_id', 'dk_league_id', 'league', 'home_team', 'away_team', 'dk_home_team_id', 'dk_away_team_id', 'match_dtime', 'db_ts']
    eventList = []

    currentDTime = sc.getCurrentDTimeEst()

    eventData = dkResponse['eventGroup']['events']
    for event in eventData:
        eventId = dk.safeParse(event, ['eventId'])
        dkLeagueId = dk.safeParse(event, ['eventGroupId'])
        league = dk.safeParse(event, ['eventGroupName'])
        homeTeam = dk.safeParse(event, ['team1', 'name'])
        awayTeam = dk.safeParse(event, ['team2', 'name'])
        dkHomeId = dk.safeParse(event, ['team1', 'teamId'])
        dkAwayId = dk.safeParse(event, ['team2', 'teamId'])
        startDate = dk.safeParse(event, ['startDate'])
        estDtFormatted = sc.convertIsoEST(startDate)
        eventList.append([eventId, dkLeagueId, league, homeTeam, awayTeam, dkHomeId, dkAwayId, estDtFormatted, currentDTime])
    
    dfEvents = pd.DataFrame(data=eventList, columns=eventSchema)

    return dfEvents


def parseDkSoccerMoneyline(dkResponse):
    '''
    Parse the soccer moneyline data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from soccer moneyline offer category dict ID values

    Returns:
        dfMoneyline: draftkings soccer moneyline dataframe
    '''

    soccerMoneylineSchema = ['dk_match_id', 'dk_league_id', 'league', 'home_team', 'home_odds', 'draw_odds', 'away_odds', 'away_team', 'dk_home_team_id', 'dk_away_team_id', 'db_ts']
    soccerMoneylineData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            eventId = dk.safeParse(game, ['eventId'])
            dkHomeId = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'id'])
            homeTeam = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'name'])
            homeOdds = dk.safeParse(game, ['outcomes', 0, 'oddsAmerican'])
            drawOdds = dk.safeParse(game, ['outcomes', 1, 'oddsAmerican'])
            awayOdds = dk.safeParse(game, ['outcomes', 2, 'oddsAmerican'])
            awayTeam = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'name'])
            dkAwayId = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'id'])
            soccerMoneylineData.append([eventId, dkLeagueId, league, homeTeam, homeOdds, drawOdds, awayOdds, awayTeam, dkHomeId, dkAwayId, currentDTime])
    
    dfMoneyline = pd.DataFrame(data=soccerMoneylineData, columns=soccerMoneylineSchema)

    return dfMoneyline


def parseDkSoccerTotals(dkResponse, totalsType):
    '''
    Parse the soccer totals data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from soccer total_{totalsType} offer category dict ID values
        totalsType: string of type of totals odds (ex: goals, corners, cards)

    Returns:
        dfTotals: draftkings soccer totals dataframe
    '''

    soccerTotalSchema = ['dk_match_id', 'dk_league_id', 'league', f'{totalsType}_under_odds', f'{totalsType}_line', f'{totalsType}_over_odds', 'db_ts']
    soccerTotalData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            eventId = game['eventId']
            for line in game['outcomes']:
                if "main" in line:
                    if line['label'] == 'Over':
                        overOdds = dk.safeParse(line, ['oddsAmerican'])
                        ouLine = dk.safeParse(line, ['line'])
                    if line['label'] == 'Under':
                        underOdds = dk.safeParse(line, ['oddsAmerican'])
                        ouLine = dk.safeParse(line, ['line'])
                else:
                    continue
        soccerTotalData.append([eventId, dkLeagueId, league, underOdds, ouLine, overOdds, currentDTime])
    
    dfTotals = pd.DataFrame(data=soccerTotalData, columns=soccerTotalSchema)

    return dfTotals


def parseDkSoccerBtts(dkResponse):
    '''
    Parse the soccer btts data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from soccer btts offer category dict ID values

    Returns:
        dfBtts: draftkings soccer btts dataframe
    '''

    soccerBttsSchema = ['dk_match_id', 'dk_league_id', 'league', 'btts_yes_odds', 'btts_no_odds', 'db_ts']
    soccerBttsData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            eventId = game['eventId']
            if game['label'] == 'Both Teams to Score':
                for line in game['outcomes']:
                    if line['label'] == 'Yes':
                        yesOdds = dk.safeParse(line, ['oddsAmerican'])
                    if line['label'] == 'No':
                        noOdds = dk.safeParse(line, ['oddsAmerican'])
            else:
                continue
        soccerBttsData.append([eventId, dkLeagueId, league, yesOdds, noOdds, currentDTime])
    
    dfBtts = pd.DataFrame(data=soccerBttsData, columns=soccerBttsSchema)

    return dfBtts


def parseDkSoccerFirstScore(dkResponse):
    '''
    Parse the soccer first score data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from soccer first_score offer category dict ID values

    Returns:
        dfFirstScore: draftkings soccer first score dataframe
    '''

    soccerFirstScoreSchema = ['dk_match_id', 'dk_league_id', 'league', 'home_team', 'home_first_score_odds', 'no_score_odds', 'away_first_score_odds', 'away_team', 'dk_home_team_id', 'dk_away_team_id', 'db_ts']
    soccerFirstScoreData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            eventId = game['eventId']
            if game['label'] == '1st Goal':
                dkHomeId = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'id'])
                homeTeam = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'name'])
                homeOdds = dk.safeParse(game, ['outcomes', 0, 'oddsAmerican'])
                noScoreOdds = dk.safeParse(game, ['outcomes', 1, 'oddsAmerican'])
                awayOdds = dk.safeParse(game, ['outcomes', 2, 'oddsAmerican'])
                awayTeam = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'name'])
                dkAwayId = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'id'])
            else:
                continue
            soccerFirstScoreData.append([eventId, dkLeagueId, league, homeTeam, homeOdds, noScoreOdds, awayOdds, awayTeam, dkHomeId, dkAwayId, currentDTime])
    
    dfFirstScore = pd.DataFrame(data=soccerFirstScoreData, columns=soccerFirstScoreSchema)

    return dfFirstScore


#*** sort order changes based on odds, need to pass through home / away teams to use in logic along with yes / no cs
def parseDkSoccerCleanSheet(dkResponse):
    '''
    Parse the soccer clean sheet data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from soccer clean_sheet offer category dict ID values

    Returns:
        dfCleanSheet: draftkings soccer clean sheet dataframe
    '''

    soccerCleanSheetSchema = ['dk_match_id', 'dk_league_id', 'league', 'home_team', 'home_cs_odds', 'home_no_cs_odds', 'away_team', 'away_cs_odds', 'away_no_cs_odds', 'dk_home_team_id', 'dk_away_team_id', 'db_ts']
    soccerCleanSheetData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            eventId = dk.safeParse(game, ['eventId'])
            dkHomeId = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'id'])
            homeTeam = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'name'])
            homeCsOdds = dk.safeParse(game, ['outcomes', 0, 'oddsAmerican'])
            homeNoCsOdds = dk.safeParse(game, ['outcomes', 2, 'oddsAmerican'])
            awayCsOdds = dk.safeParse(game, ['outcomes', 1, 'oddsAmerican'])
            awayNoCsOdds = dk.safeParse(game, ['outcomes', 3, 'oddsAmerican'])
            awayTeam = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'name'])
            dkAwayId = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'id'])
            # eventId = dk.safeParse(game, ['eventId'])
            # dkHomeId = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'id'])
            # homeTeam = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'name'])
            # homeCsOdds = dk.safeParse(game, ['outcomes', 1, 'oddsAmerican'])
            # homeNoCsOdds = dk.safeParse(game, ['outcomes', 2, 'oddsAmerican'])
            # awayCsOdds = dk.safeParse(game, ['outcomes', 0, 'oddsAmerican'])
            # awayNoCsOdds = dk.safeParse(game, ['outcomes', 3, 'oddsAmerican'])
            # awayTeam = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'name'])
            # dkAwayId = dk.safeParse(game, ['outcomes', 3, 'participants', 0, 'id'])
        soccerCleanSheetData.append([eventId, dkLeagueId, league, homeTeam, homeCsOdds, homeNoCsOdds, awayTeam, awayCsOdds, awayNoCsOdds, dkHomeId, dkAwayId, currentDTime])

    dfCleanSheet = pd.DataFrame(data=soccerCleanSheetData, columns=soccerCleanSheetSchema)

    return dfCleanSheet


def parseDkSoccerHalfMoneyline(dkResponse):
    '''
    Parse the soccer half moneyline data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from soccer half_moneyline offer category dict ID values

    Returns:
        dfHalfMoneyline: draftkings soccer half moneyline dataframe
    '''

    soccerHalfMoneylineSchema = ['dk_match_id', 'dk_league_id', 'league', 'home_team', 'home_half_odds', 'draw_half_odds', 'away_half_odds', 'away_team', 'dk_home_team_id', 'dk_away_team_id', 'db_ts']
    soccerHalfMoneylineData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            eventId = game['eventId']
            if game['label'] == 'Moneyline 1st Half':
                dkHomeId = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'id'])
                homeTeam = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'name'])
                homeOdds = dk.safeParse(game, ['outcomes', 0, 'oddsAmerican'])
                drawOdds = dk.safeParse(game, ['outcomes', 1, 'oddsAmerican'])
                awayOdds = dk.safeParse(game, ['outcomes', 2, 'oddsAmerican'])
                awayTeam = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'name'])
                dkAwayId = dk.safeParse(game, ['outcomes', 2, 'participants', 0, 'id'])
            else:
                continue
            soccerHalfMoneylineData.append([eventId, dkLeagueId, league, homeTeam, homeOdds, drawOdds, awayOdds, awayTeam, dkHomeId, dkAwayId, currentDTime])

    dfHalfMoneyline = pd.DataFrame(data=soccerHalfMoneylineData, columns=soccerHalfMoneylineSchema)

    return dfHalfMoneyline