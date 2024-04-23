import streamlit as st
from Pipelines.espn import adp
import warnings


warnings.filterwarnings("ignore")


def inputPlayerResultSize():
    '''
    Input of the player result size by the user to use in API call

    Returns:
        resultSize: number of players
    '''

    if resultSize := st.text_input("Input the number of players to pull based on the draft room rank order: "):
        return resultSize
    else:
        st.stop()


def loadEspnData(resultSize):
    '''
    Call ESPN API and parse JSON into dataframe

    Args:
        resultSize: number of players to request
    
    Returns:
        espnDf: dataframe of ESPN ADP and projection data
    '''

    espnResponse = adp.getEspnAdpProj(resultSize)
    espnDf = adp.parseEspnAdpProj(espnResponse)

    return espnDf


def loadEspnPosList(espnDf):
    '''
    Load list of positions for selection by the user

    Args:
        espnDf: dataframe of ESPN ADP and projection data
    
    Returns:
        positions: list of player positions
    '''

    positions = espnDf['position'].unique()

    return positions


def selectEspnPos(positions):
    '''
    Selection of position / positions by user

    Args:
        positions: list of positions

    Returns:
        selectedPositions: list of selected positions
    '''

    selectedPositions = st.multiselect('Select one or more positions: ', positions)

    if selectedPositions is None:
        st.stop()

    return selectedPositions


def filterPosEspnData(espnDf, selectedPositions):
    '''
    Filter data for selected positions

    Args:
        espnDf: dataframe of ESPN ADP and projection data
        selectedPositions: list of selected positions

    Returns:
        posEspnDf: dataframe of ESPN ADP and projection data filtered by selected positions
    '''

    posEspnDf = espnDf[espnDf['position'].isin(selectedPositions)]

    return posEspnDf


def rankEspnData(posEspnDf):
    '''
    Add ranking columns to ESPN data

    Args:
        posEspnDf: dataframe of ESPN ADP and projection data filtered by selected positions
    
    Returns:
        posEspnDf: dataframe of ESPN ADP and projection data filtered by selected positions with rankings columns
    '''

    posEspnDf['adp_rank'] = posEspnDf['espn_adp'].rank(ascending=True)
    posEspnDf['proj_rank'] = posEspnDf['proj_points'].rank(ascending=False)
    posEspnDf['pos_rank'] = posEspnDf.groupby('position')['proj_points'].rank(ascending=False)

    return posEspnDf


def espnDataSchema():
    '''
    Create lists for the ESPN data schema and displaySchema

    Returns:
        schema: list of columns for ESPN data ordering
        displaySchema: list of columns to rename ESPN data for display in UI
    '''

    schema = ['espn_rank', 'player', 'team', 'adp_rank', 'espn_adp',
    'pos_rank', 'position', 'proj_rank', 'proj_points',
    'pass_att', 'pass_comp', 'pass_yds', 'pass_td', 'int', 
    'carries', 'rush_yds', 'rush_td', 
    'targets', 'receptions', 'rec_yds', 'rec_td']
    #, 'proj_ppg']

    displaySchema = ['Draft Rank', 'Player', 'Team', 'ADP Rank', 'ADP',
    'Pos Rank', 'Pos', 'Proj Rank', 'Proj Points',
    'Pass Att', 'Pass Comp', 'Pass Yds', 'Pass TD', 'INT', 
    'Carries', 'Rush Yds', 'Rush TD', 
    'Targets', 'Rec', 'Rec Yds', 'Rec TD']

    return schema, displaySchema


def dropZeroedCols(espnDfDisplay):
    '''
    Drop columns if more than 90% of the rows are 0 for easier visibility
    (ex: if RB and WR selected, passing and QB related columns would be dropped)

    Args:
        espnDfDisplay: dataframe of ESPN ADP and projection data with named columns

    Returns:
        espnDfDisplay: dataframe of ESPN ADP and projection data with named columns and unapplicable columns dropped
    '''

    totalRows = len(espnDfDisplay)
    threshold = 0.9 * totalRows

    columnsDrop = []

    for column in espnDfDisplay.columns:
        if (espnDfDisplay[column] == 0).sum() > threshold:
            columnsDrop.append(column)

    espnDfDisplay.drop(columns=columnsDrop, inplace=True)

    return espnDfDisplay


def roundStats(cleanedEspnDf):
    '''
    Rounds stats in ESPN ADP and projection data to two decimal places

    Args:
        cleanedEspnDf: dataframe of ESPN ADP and projection data with named columns and unapplicable columns dropped

    Returns:
        cleanedEspnDf: dataframe of ESPN ADP and projection data with rounded statistics
    '''

    for column in cleanedEspnDf.select_dtypes(include=['float64', 'int64']).columns:
        cleanedEspnDf[column] = cleanedEspnDf[column].round(2)

    return cleanedEspnDf


def cleanEspnDataDf(espnDfRanked):
    '''
    Clean and round ESPN ADP and projection data

    Args:
        espnDfRanked: dataframe of ESPN ADP and projection data with ranking columns

    Returns:
        roundedEspnDf: dataframe of ESPN ADP and projection data with named columns and rounded statistics
    '''

    schema, displaySchema = espnDataSchema()
    espnDfDisplay = espnDfRanked[schema]
    espnDfDisplay.columns = displaySchema

    cleanedEspnDf = dropZeroedCols(espnDfDisplay)
    roundedEspnDf = roundStats(cleanedEspnDf)

    return roundedEspnDf


def espnAdpValues():
    '''
    Execute ESPN ADP and projections values app
    '''

    resultSize = inputPlayerResultSize()
    espnDf = loadEspnData(resultSize)
    positions = loadEspnPosList(espnDf)
    selectedPositions = selectEspnPos(positions)
    posEspnDf = filterPosEspnData(espnDf, selectedPositions)
    espnDfRanked = rankEspnData(posEspnDf)
    
    if not espnDfRanked.empty:
        espnDfClean = cleanEspnDataDf(espnDfRanked)
        st.dataframe(espnDfClean, use_container_width = True, hide_index = True)