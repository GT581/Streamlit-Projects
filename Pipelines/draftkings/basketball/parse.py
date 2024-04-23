import Pipelines.sports_common as sc
import Pipelines.draftkings.common as dk
import pandas as pd


def parseDkBasketballEvents(dkResponse):
    '''
    Parse the basketball event data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from basketball events offer category dict ID values

    Returns:
        dfEvents: draftkings basketball event dataframe
    '''

    eventSchema = ['dk_match_id', 'dk_league_id', 'league', 'home_team', 'away_team', 'dk_home_team_id', 'dk_away_team_id', 'match_dtime', 'db_ts']
    eventList = []

    currentDTime = sc.getCurrentDTimeEst()

    eventData = dkResponse['eventGroup']['events']
    for event in eventData:
        eventId = dk.safeParse(event, ['eventId'])
        dkLeagueId = dk.safeParse(event, ['eventGroupId'])
        league = dk.safeParse(event, ['eventGroupName'])
        homeTeam = dk.safeParse(event, ['team2', 'name'])
        awayTeam = dk.safeParse(event, ['team1', 'name'])
        dkHomeId = dk.safeParse(event, ['team2', 'teamId'])
        dkAwayId = dk.safeParse(event, ['team1', 'teamId'])
        startDate = dk.safeParse(event, ['startDate'])
        estDtFormatted = sc.convertIsoEST(startDate)
        eventList.append([eventId, dkLeagueId, league, homeTeam, awayTeam, dkHomeId, dkAwayId, estDtFormatted, currentDTime])
    
    dfEvents = pd.DataFrame(data=eventList, columns=eventSchema)

    return dfEvents


def parseDkBasketballMoneyline(dkResponse):
    '''
    Parse the basketball moneyline data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from basketball moneyline offer category dict ID values

    Returns:
        dfMoneyline: draftkings basketball moneyline dataframe
    '''

    basketballMoneylineSchema = ['dk_match_id', 'dk_league_id', 'league', 'home_team', 'home_odds', 'away_odds', 'away_team', 'dk_home_team_id', 'dk_away_team_id', 'db_ts']
    basketballMoneylineData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            eventId = dk.safeParse(game, ['eventId'])
            dkHomeId = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'id'])
            homeTeam = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'name'])
            homeOdds = dk.safeParse(game, ['outcomes', 1, 'oddsAmerican'])
            awayOdds = dk.safeParse(game, ['outcomes', 0, 'oddsAmerican'])
            awayTeam = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'name'])
            dkAwayId = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'id'])
        basketballMoneylineData.append([eventId, dkLeagueId, league, homeTeam, homeOdds, awayOdds, awayTeam, dkHomeId, dkAwayId, currentDTime])
    
    dfMoneyline = pd.DataFrame(data=basketballMoneylineData, columns=basketballMoneylineSchema)

    return dfMoneyline


def parseDkBasketballTotals(dkResponse, totalsType):
    '''
    Parse the basketball totals data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from basketball total_{totalsType} offer category dict ID values
        totalsType: string of type of totals odds (ex: points)

    Returns:
        dfTotals: draftkings basketball totals dataframe
    '''

    basketballTotalSchema = ['dk_match_id', 'dk_league_id', 'league', f'{totalsType}_under_odds', f'{totalsType}_line', f'{totalsType}_over_odds', 'db_ts']
    basketballTotalData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            eventId = game['eventId']
            for line in game['outcomes']:
                if "label" in line and "main" in line:
                    if line['label'] == 'Over':
                        overOdds = dk.safeParse(line, ['oddsAmerican'])
                        ouLine = dk.safeParse(line, ['line'])
                    if line['label'] == 'Under':
                        underOdds = dk.safeParse(line, ['oddsAmerican'])
                        ouLine = dk.safeParse(line, ['line'])
                else:
                    continue
        basketballTotalData.append([eventId, dkLeagueId, league, underOdds, ouLine, overOdds, currentDTime])
    
    dfTotals = pd.DataFrame(data=basketballTotalData, columns=basketballTotalSchema)

    return dfTotals


def parseDkBasketballSpreads(dkResponse):
    '''
    Parse the basketball spread data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from basketball spread offer category dict ID values

    Returns:
        dfSpreads: draftkings basketball spread dataframe
    '''

    basketballSpreadsSchema = ['dk_match_id', 'dk_league_id', 'league', 'home_team', 'home_spread', 'home_spread_odds', 'away_spread_odds', 'away_spread', 'away_team', 'dk_home_team_id', 'dk_away_team_id', 'db_ts']
    basketballSpreadsData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            if "label" in game and game['label'] == 'Spread':
                eventId = game['eventId']
                if "main" in game['outcomes'][0]:
                    dkHomeId = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'id'])
                    homeTeam = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'name'])
                    homeOdds = dk.safeParse(game, ['outcomes', 1, 'oddsAmerican'])
                    homeSpread = dk.safeParse(game, ['outcomes', 1, 'line'])
                    awaySpread = dk.safeParse(game, ['outcomes', 0, 'line'])
                    awayOdds = dk.safeParse(game, ['outcomes', 0, 'oddsAmerican'])
                    awayTeam = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'name'])
                    dkAwayId = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'id'])
                else:
                    continue
            else:
                continue
            basketballSpreadsData.append([eventId, dkLeagueId, league, homeTeam, homeSpread, homeOdds, awayOdds, awaySpread, awayTeam, dkHomeId, dkAwayId, currentDTime])
    
    dfSpreads = pd.DataFrame(data=basketballSpreadsData, columns=basketballSpreadsSchema)

    return dfSpreads


def parseDkBasketballHalfMoneyline(dkResponse):
    '''
    Parse the basketball half moneyline data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from basketball half_moneyline offer category dict ID values

    Returns:
        dfHalfMoneyline: draftkings basketball half moneyline dataframe
    '''

    basketballHalfMoneylineSchema = ['dk_match_id', 'dk_league_id', 'league', 'home_team', 'home_half_odds', 'away_half_odds', 'away_team', 'dk_home_team_id', 'dk_away_team_id', 'db_ts']
    basketballHalfMoneylineData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            eventId = game['eventId']
            if "label" in game and game['label'] == 'Moneyline 1st Half':
                dkHomeId = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'id'])
                homeTeam = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'name'])
                homeOdds = dk.safeParse(game, ['outcomes', 1, 'oddsAmerican'])
                awayOdds = dk.safeParse(game, ['outcomes', 0, 'oddsAmerican'])
                awayTeam = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'name'])
                dkAwayId = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'id'])
            else:
                continue
            basketballHalfMoneylineData.append([eventId, dkLeagueId, league, homeTeam, homeOdds, awayOdds, awayTeam, dkHomeId, dkAwayId, currentDTime])

    dfHalfMoneyline = pd.DataFrame(data=basketballHalfMoneylineData, columns=basketballHalfMoneylineSchema)

    return dfHalfMoneyline


def parseDkBasketballQtrMoneyline(dkResponse):
    '''
    Parse the basketball qtr moneyline data from the draftkings API JSON

    Args:
        dkResponse: dkResponse from basketball qtr_moneyline offer category dict ID values

    Returns:
        dfQtrMoneyline: draftkings basketball qtr moneyline dataframe
    '''

    basketballQtrMoneylineSchema = ['dk_match_id', 'dk_league_id', 'league', 'home_team', 'home_qtr_odds', 'away_qtr_odds', 'away_team', 'dk_home_team_id', 'dk_away_team_id', 'db_ts']
    basketballQtrMoneylineData = []

    league = dkResponse['eventGroup']['name']
    dkLeagueId = dkResponse['eventGroup']['eventGroupId']
    currentDTime = sc.getCurrentDTimeEst()

    offers = dk.parseOffers(dkResponse)
    for offer in offers:
        for game in offer:
            eventId = game['eventId']
            if "label" in game and game['label'] == 'Moneyline 1st Quarter':
                dkHomeId = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'id'])
                homeTeam = dk.safeParse(game, ['outcomes', 1, 'participants', 0, 'name'])
                homeOdds = dk.safeParse(game, ['outcomes', 1, 'oddsAmerican'])
                awayOdds = dk.safeParse(game, ['outcomes', 0, 'oddsAmerican'])
                awayTeam = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'name'])
                dkAwayId = dk.safeParse(game, ['outcomes', 0, 'participants', 0, 'id'])
            else:
                continue
            basketballQtrMoneylineData.append([eventId, dkLeagueId, league, homeTeam, homeOdds, awayOdds, awayTeam, dkHomeId, dkAwayId, currentDTime])

    dfQtrMoneyline = pd.DataFrame(data=basketballQtrMoneylineData, columns=basketballQtrMoneylineSchema)

    return dfQtrMoneyline