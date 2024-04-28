import requests
import pandas as pd
from bs4 import BeautifulSoup
import re


def fantasyProsUrls():
    urlsDict = {
    "football": [
    {'flexProj': 'https://www.fantasypros.com/nfl/projections/flex.php?week=draft&scoring=PPR&week=draft'},
    {'qbProj': 'https://www.fantasypros.com/nfl/projections/qb.php?week=draft'},
    {'adp': 'https://www.fantasypros.com/nfl/adp/ppr-overall.php'}
    ]
    }
    return urlsDict


def scrapeFantasyProsTable(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='table')
    headers = [th.text.strip() for th in table.find_all('th')]
    data = []
    for tr in table.find_all('tr')[1:]:
        row = [td.text.strip() for td in tr.find_all('td')]
        data.append(row)
    df = pd.DataFrame(data, columns=headers)
    df = df.dropna()
    df = df.reset_index(drop=True)
    return df


def createFantasyProsDf(link):
    urlDict = fantasyProsUrls()
    url = urlDict[link]
    df = scrapeFantasyProsTable(url)
    return df


def renameFantasyProsColumns(df, columnMapping):
    df.rename(columns=columnMapping, inplace=True)
    return df


def stripCreateFantasyProsPosition(df):
    df['position'] = df['POS'].str.replace('\d+', '', regex=True)
    posIndex = df.columns.get_loc("POS")
    df.insert(posIndex, "position", df.pop("position"))
    return df


def stripTeam(player):
    match = re.search(r'\(([A-Z]+)\)', player)
    if match:
        return match.group(1)
    else:
        return None


def convertDecimal(percentage):
    if isinstance(percentage, pd.Series):
        return percentage.str.strip('%').astype(float) / 100
    if percentage.strip('%').isdigit():
        return float(percentage.strip('%')) / 100
    else:
        return 0