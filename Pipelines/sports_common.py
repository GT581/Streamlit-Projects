from datetime import datetime
import pytz
# import os
# import sqlalchemy
# from sqlalchemy import create_engine, text
# import os
# from dotenv import load_dotenv


def genFormattedDate():
    '''
    Get current date as string to use in sofascore scheduled events api endpoint

    Returns: 
        formattedDate: string of current date in YYYY-mm-dd format
    '''

    currentDate = datetime.now()
    formattedDate = currentDate.strftime("%Y-%m-%d")

    return formattedDate


def getCurrentDTimeEst():
    '''
    Get current datetime in EST to use in local postgres db / loaded dataframe

    Returns: 
        formattedEst: string of current datetime in YYYY-mm-dd HH-MM-SS format
    '''

    utcNow = datetime.now()
    est = pytz.timezone('US/Eastern')
    estNow = utcNow.astimezone(est)
    formattedEst = estNow.strftime("%Y-%m-%d %H:%M:%S")

    return formattedEst


def convertIsoEST(startDate):
    '''
    Convert ISO time values in draftkings API data to EST to match sofascore match times

    Args: 
        startDate: Value of startDate key in draftkings API

    Returns: 
        estDtFormatted: string of match datetime in YYYY-mm-dd HH-MM-SS format
    '''
    timestampStr = startDate[:-5]
    timestamp = datetime.fromisoformat(timestampStr)
    utcTimezone = pytz.timezone('UTC')
    timestamp = utcTimezone.localize(timestamp)
    estTimezone = pytz.timezone('US/Eastern')
    estTime = timestamp.astimezone(estTimezone)
    estDtFormatted = estTime.strftime('%Y-%m-%d %H:%M:%S')

    return estDtFormatted


# def convertIso(startDate):
#     timestampStr = startDate[:-5]
#     timestamp = datetime.fromisoformat(timestampStr)
#     utcTimezone = pytz.timezone('UTC')
#     timestamp = utcTimezone.localize(timestamp)
#     dtFormatted = timestamp.strftime('%Y-%m-%d %H:%M:%S')
#     return dtFormatted


# #Convert UTC timestamp data from api to EST
# def convertUnixEST(startTimestamp):
#     utc_dt = datetime.utcfromtimestamp(startTimestamp)
#     est = pytz.timezone('US/Eastern')
#     est_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(est)
#     est_dt_formatted = est_dt.strftime('%Y-%m-%d %H:%M:%S')
#     return est_dt_formatted


#Keeping same name as EST but UTC   **to change
def convertUnixEST(startTimestamp):
    '''
    Convert Unix time values in sofascore API to match draftkings match times

    Args: 
        startTimestamp: Value of startTimestamp key in sofascore API

    Returns: 
        dtFormatted: string of match datetime in YYYY-mm-dd HH-MM-SS format
    '''

    dtFormatted = datetime.fromtimestamp(startTimestamp).strftime('%Y-%m-%d %H:%M:%S')

    return dtFormatted


# #Create connection to the local postgres database
# def createSqlEngine():
#     load_dotenv()
#     databaseStr = os.environ.get('SPORTS_DATABASE_URL')
#     sqlEngine = sqlalchemy.create_engine(databaseStr)
#     return sqlEngine


# #Write dataframe parsed from response to stage table in database
# def writeStage(df, table, sport, dbSchema, schema):
#     engine = createSqlEngine()
#     df.to_sql(f'{sport}_{table}_stage', engine, schema = dbSchema, if_exists = 'append', dtype = schema, index = False)
#     print(f'{sport}_{table} data loaded into database')


# #Execute SQL files used for CDC / updates
# def executeCdc(sport, dbSchema, table):
#     engine = createSqlEngine()
#     load_dotenv()
#     cdcSqlPath = os.environ.get('CDC_SQL_PATH')
#     sqlFilePath = f'{cdcSqlPath}/{dbSchema}/{sport}/{sport}_{table}_cdc.sql'
#     with open(sqlFilePath, 'r') as file:
#         sqlQuery = file.read()
#     with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
#         with connection.begin():
#          connection.execute(text(sqlQuery))
#     print(f'{sport}_{table} CDC executed')


# #Execute CDC SQL script for the flattened table bringing DK / Sofascore data together for each event, aligning odds with bet category streaks
# def executeScreenerCdc(sportList):
#     dbSchema = 'streaks_screener'
#     load_dotenv()
#     cdcSqlPath = os.environ.get('CDC_SQL_PATH')
#     engine = createSqlEngine()
#     for sport in sportList:
#         sqlFilePath = f'{cdcSqlPath}/{dbSchema}/{sport}/{sport}_cdc.sql'
#         with open(sqlFilePath, 'r') as file:
#             sqlQuery = file.read()
#         with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
#             with connection.begin():
#              connection.execute(text(sqlQuery))
#         print(f'{sport} screener CDC executed')