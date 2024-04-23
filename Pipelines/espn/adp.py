import requests
import pandas as pd
import Pipelines.espn.config as config


def getEspnAdpProj(resultSize):
    '''
    Get request to retrieve ADP and Projection data for fantasy football from the ESPN API

    Args: 
        resultSize: number of players to return from ESPN request

    Returns: 
        espnResponse: ESPN espnResponse JSON
    '''

    url = "https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/2024/segments/0/leaguedefaults/3?scoringPeriodId=0&view=kona_player_info"

    payload = {}

    headers = {
      'authority': 'lm-api-reads.fantasy.espn.com',
      'accept': 'application/json',
      'accept-language': 'en-US,en;q=0.9',
      'cookie': 'AMCVS_EE0201AC512D2BE80A490D4C%40AdobeOrg=1; s_ecid=MCMID%7C41299001466571937541354566337687744004; country=us; s_vi=[CS]v1|3258D9FBF7CCEA3F-400006C4C800132E[CE]; s_pers=%20s_c24%3D1689367545794%7C1783975545794%3B%20s_c24_s%3DLess%2520than%25207%2520days%7C1689369345794%3B%20s_gpv_pn%3Despn%253Aespn%253Alatestnews%7C1689369345801%3B; s_sess=%20s_cc%3Dtrue%3B%20s_ppv%3D12%3B%20s_omni_lid%3Dsitenavdefault%252Bsitenav_main-logo%255Eespn%253Aespn%253Alatestnews%3B%20s_sq%3Dwdgespcom%252Cwdgespge%253D%252526pid%25253Despn%2525253Aespn%2525253Alatestnews%252526pidt%25253D1%252526oid%25253Dhttp%2525253A%2525252F%2525252Fwww.espn.com%2525252F%252526ot%25253DA%3B; s_cc=true; espn_s2=AEAn%2FvlqkC%2BL%2ByrMkATyHOuHKR3Id%2FwjN%2FYAbFD71%2BRl0%2F4HQ6fokR6ANt9gI8%2FLn6rqvcUgcU2uitynuijpxiVxsPmBeWCit9q%2FENAZUqwO41Szigzsjf9EpggvDSermSElknzlQkRQR0GLkdIq6jFf4fjC9QqlY%2FLBQN9YsyDAQm8Tq5pX20Q%2FBUpbQwdHkmpBBD9bsz2VeIgYPshDhDFeM5hDTG9ade3hSz7wBeB0OWIoovirCPiPIam%2F8FXp9QYUZn3idp4qf0blIv0n3ECnv9jAHFj2vRakqwdF7xIl%2Bw%3D%3D; SWID=522c30d1-be00-45da-8c22-d3ee4c9af9fb; ESPN-ONESITE.WEB-PROD.api=gamyZGA+AwqJA0V1z+8o5y+wpy+RpvCEHXd3jDW5naw0lE4LVovKP3/RRWs0atK9Ch7xVIOul5ttTBtXJMUAdVZlI37z; userZip=06033; tveAuth=; tveMVPDAuth=; check=true; _cb=BplFOYDgmnj_Sou4-; IR_gbd=espn.com; _omnicwtest=works; hashedIp=af1a438ce40ae3abcbaf30d462f7bb3483dfc945c72f68d2905ffe98c1c2b479; s_omni_lid=%5B%5BB%5D%5D; nol_fpid=qvjehfbqbztqf93gzgodk2it2nx9n1713325899|1713325899292|1713330193904|1713330193931; s_c24_s=Less%20than%201%20day; mbox=PC#404a6c35861f44c7b07280e9d04f69b5.34_0#1776617423|session#c0175f6c2c1c45faa44779dc6df9068b#1713374483; block.check=true%7Cfalse; AMCV_EE0201AC512D2BE80A490D4C%40AdobeOrg=-330454231%7CMCIDTS%7C19831%7CMCMID%7C41299001466571937541354566337687744004%7CMCAAMLH-1713977423%7C7%7CMCAAMB-1713977423%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1713379823s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; ab.storage.sessionId.96ad02b7-2edc-4238-8442-bc35ba85853c=%7B%22g%22%3A%22f2c42ac6-34af-737d-db21-543ad66b6673%22%2C%22e%22%3A1713374424190%2C%22c%22%3A1713372624191%2C%22l%22%3A1713372624191%7D; ab.storage.deviceId.96ad02b7-2edc-4238-8442-bc35ba85853c=%7B%22g%22%3A%228a1c9879-0c0d-efee-ae50-8c50e2f5c281%22%2C%22c%22%3A1666323534239%2C%22l%22%3A1713372624191%7D; ab.storage.userId.96ad02b7-2edc-4238-8442-bc35ba85853c=%7B%22g%22%3A%22522c30d1-be00-45da-8c22-d3ee4c9af9fb%22%2C%22c%22%3A1713325878197%2C%22l%22%3A1713372624192%7D; s_ensNR=1713373908957-Repeat; OptanonConsent=isIABGlobal=false&datestamp=Wed+Apr+17+2024+13%3A11%3A49+GMT-0400+(Eastern+Daylight+Time)&version=202310.1.0&hosts=&consentId=fd3517b9-fb01-4a61-86e4-d405da361385&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0005%3A1%2CBG1145%3A1&AwaitingReconsent=false&isGpcEnabled=0&browserGpcFlag=0; _chartbeat2=.1644374761411.1713373909298.0000000000000011.DgMJdwCAJTj1DS86sUCHiadoBjglGp.1; _cb_svref=https%3A%2F%2Fwww.espn.com%2F; IR_9070=1713373909418%7C0%7C1713373909418%7C%7C; s_gpv_pn=fantasy%3Afootball%3Aleague%3Atoolsprojections; s_c6=1713373910258-Repeat; FCNEC=%5B%5B%22AKsRol8-1-_1G75dM-XqqqBE7lb9EwQqnB3vgOcjLtFna5ByCNsmD4pShhIsNqXIb2ci8IKgYVSHWHPL7l1xTBkr3IUI-WdMO8R6rfts6nlTLvbNkNxOEPZEz-CBSBRNFjpYs7Uw-Nlx4JmZnPpbq5xlxVr6xhyqPg%3D%3D%22%5D%5D; s_sq=wdgespcom%252Cwdgespge%3D%2526pid%253Dfantasy%25253Afootball%25253Aleague%25253Atoolsprojections%2526pidt%253D1%2526oid%253Dfunctionmr%252528%252529%25257B%25257D%2526oidt%253D2%2526ot%253DSUBMIT; s_c24=1713375112041',
      'if-none-match': '"07a61cdd7a1948b774f41f0641deca824"',
      'origin': 'https://fantasy.espn.com',
      'referer': 'https://fantasy.espn.com/',
      'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
      #'x-fantasy-filter': '{"players":{"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"filterStatsForExternalIds":{"value":[2024]},"filterStatsForSourceIds":{"value":[1]},"sortAppliedStatTotal":{"sortAsc":false,"sortPriority":3,"value":"102024"},"sortDraftRanks":{"sortPriority":2,"sortAsc":true,"value":"PPR"},"sortPercOwned":{"sortAsc":false,"sortPriority":4},"limit":300,"offset":0,"filterRanksForScoringPeriodIds":{"value":[1]},"filterRanksForRankTypes":{"value":["PPR"]},"filterRanksForSlotIds":{"value":[0,2,4,6,17,16,8,9,10,12,13,24,11,14,15]},"filterStatsForTopScoringPeriodIds":{"value":2,"additionalValue":["002024","102024","002023","022024"]}}}',
      'x-fantasy-filter': '{"players":{"filterSlotIds":{"value":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,23,24]},"filterStatsForExternalIds":{"value":[2024]},"filterStatsForSourceIds":{"value":[1]},"sortAppliedStatTotal":{"sortAsc":false,"sortPriority":3,"value":"102024"},"sortDraftRanks":{"sortPriority":2,"sortAsc":true,"value":"PPR"},"sortPercOwned":{"sortAsc":false,"sortPriority":4},"limit":' + resultSize + ',"offset":0,"filterRanksForScoringPeriodIds":{"value":[1]},"filterRanksForRankTypes":{"value":["PPR"]},"filterRanksForSlotIds":{"value":[0,2,4,6,17,16,8,9,10,12,13,24,11,14,15]},"filterStatsForTopScoringPeriodIds":{"value":2,"additionalValue":["002024","102024","002023","022024"]}}}',
      'x-fantasy-platform': 'kona-PROD-171ba015edf7ad163f6be53c993448794f456934',
      'x-fantasy-source': 'kona'
    }

    espnResponse = requests.request("GET", url, headers=headers, data=payload).json()

    return espnResponse


def mapEspnStats(statDict, playerStats):
    '''
    Map ESPN statistic IDs and data in the JSON to their names as defined in mapping dict

    Args: 
        statDict: mapping dict of ESPN IDs to their statistics
        playerStats: dict of player's stats from ESPN API

    Returns:
        mappedStats: dict of stats with mapped names
    '''

    mappedStats = {}

    for key, value in playerStats.items():
        try:
            mappedStats[statDict[key]] = value
        except:
            continue
    
    return mappedStats


def parseEspnAdpProj(espnResponse):
    '''
    Parse the ESPN API ADP and projections JSON
    
    Args:
        espnResponse: espnResponse JSON from getEspnAdpProj

    Returns:
        playersDf: Dataframe of ESPN players adp and projections data
    '''

    playerSchema = ['espn_adp', 'player', 'team', 'position', 'pass_att', 'pass_comp', 'pass_yds', 'pass_td', 'int', 
    'carries', 'rush_yds', 'rush_td', 'rec_yds', 'rec_td', 'receptions', 'targets', 'proj_ppg', 'proj_points']
    playerList = []

    posDict = config.espnPositionMapping()
    statDict = config.espnProjStatsMapping()
    teamDict = config.espnNflTeamMapping()

    #Iterate through each player dict in the players list
    for d in espnResponse['players']:

        posMapNum = d['player']['defaultPositionId']
        teamMapNum = d['player']['proTeamId']

        #FA, DST, K won't have player stats
        try:
            playerStats = d['player']['stats'][0]['stats']
        except:
            continue

        mappedStats = mapEspnStats(statDict, playerStats)
        position = posDict[posMapNum]
        team = teamDict[teamMapNum]
        player = d['player']['fullName']
        adp = d['player']['ownership']['averageDraftPosition']
        projPPG = d['player']['stats'][0]['appliedAverage']
        projPoints = d['player']['stats'][0]['appliedTotal']

        passAtt = mappedStats.get('pass_att', 0)
        passComp = mappedStats.get('pass_comp', 0)
        passYds = mappedStats.get('pass_yds', 0)
        passTd = mappedStats.get('pass_td', 0)
        int = mappedStats.get('int', 0)
        carries = mappedStats.get('carries', 0)
        rushYds = mappedStats.get('rush_yds', 0)
        rushTd = mappedStats.get('rush_td', 0)
        recYds = mappedStats.get('rec_yds', 0)
        recTd = mappedStats.get('rec_td', 0)
        receptions = mappedStats.get('receptions', 0)
        targets = mappedStats.get('targets', 0)

        playerList.append([adp, player, team, position, passAtt, passComp, passYds, passTd, int,
        carries, rushYds, rushTd, recYds,recTd, receptions, targets, projPPG, projPoints])
    
    playersDf = pd.DataFrame(data=playerList, columns=playerSchema)

    #Assign row number to represnt order of players in API call / as in draft room as the "ESPN Rank" based on index of dataframe
    playersDf.reset_index(drop=False, inplace=True)
    playersDf['index'] += 1
    playersDf.rename(columns={'index': 'espn_rank'}, inplace=True)

    return playersDf