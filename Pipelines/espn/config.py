#Mapping dicts for ESPN API IDs


def espnPositionMapping():
    '''
    Load mapping dict of ESPN API position IDs to their positions

    Returns: 
        dict for ESPN player position mapping
    '''

    posDict = {
        1: "QB",
        2: "RB",
        3: "WR",
        4: "TE",
        16: "DST",
        5: "K"
    }

    return posDict


def espnProjStatsMapping():
    '''
    Load mapping dict of ESPN API statistic IDs to their statistics

    Returns: 
        dict for ESPN player statistic mapping
    '''

    statsDict = {
        "0": 'pass_att',
        "1": 'pass_comp',
        "3": 'pass_yds',
        "4": 'pass_td',
        "20": 'int',
        "23": 'carries',
        "24": 'rush_yds',
        "25": 'rush_td',
        "42": 'rec_yds',
        "43": 'rec_td',
        "53": 'receptions',
        "58": 'targets'
    }

    return statsDict


def espnNflTeamMapping():
    '''
    Load mapping dict of ESPN API NFL team IDs to their team abbreviations

    Returns: 
        dict for ESPN NFL team mapping
    '''

    teamDict = {
        0: "FA",
        1: "ATL",
        2: "BUF",
        3: "CHI",
        4: "CIN",
        5: "CLE",
        6: "DAL",
        7: "DEN",
        8: "DET",
        9: "GB",
        10: "TEN",
        11: "IND",
        12: "KC",
        13: "LV",
        14: "LAR",
        15: "MIA",
        16: "MIN",
        17: "NE",
        18: "NO",
        19: "NYG",
        20: "NYJ",
        21: "PHI",
        22: "ARI",
        23: "PIT",
        24: "LAC",
        25: "SF",
        26: "SEA",
        27: "TB",
        28: "WAS",
        29: "CAR",
        30: "JAX",
        #31: "",
        #32: "",
        33: "BAL",
        34: "HOU"
    }

    return teamDict