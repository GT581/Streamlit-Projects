#import Pipelines.sports_common as sc
import requests


def getDkData(eventGroup, offerCategoryId, subCategoryId):
    '''
    Get request to retrieve data for a given event group, offer category, and sub category from the draftkings API

    Args: 
        eventGroup: draftkings event group ID (ex: 40253 (England - Premier League))
        offerCategoryId: draftkings offer category ID (ex: 490 (Soccer - Game Lines))
        subCategoryId: draftkings sub category ID (ex: 4514 (Soccer - Game Lines - Moneyline))

    Returns: 
        dkResponse: draftkings dkResponse JSON
    '''

    url = f"https://sportsbook.draftkings.com/sites/US-SB/api/v5/eventgroups/{eventGroup}/categories/{offerCategoryId}/subcategories/{subCategoryId}?format=json"

    headers = {
    'authority': 'sportsbook.draftkings.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    dkResponse = requests.request("GET", url, headers=headers).json()

    return dkResponse


def parseOffers(dkResponse):
    '''
    Common function for parsing DK responses down to the "offer" level containing matches, teams, lines and odds

    Args: 
        dkResponse: dkResponse JSON from getDkData

    Returns: 
        offers: draftkings dkResponse JSON at the offers list level
    '''

    offerCategories = dkResponse['eventGroup']['offerCategories']
    for cat in offerCategories:
        if 'offerSubcategoryDescriptors' in cat:
            subCatDesc = cat['offerSubcategoryDescriptors']
            for subCat in subCatDesc:                
                if 'offerSubcategory' in subCat:
                    offers = subCat['offerSubcategory']['offers']
                    return offers


def safeParse(data, keys, default=None):
    '''
    Common function for parsing DK responses, returns None if error parsing through odds not offered for some events or that are not yet available

    Args: 
        data: game dict
        keys: keys to parse from game dict
        default: None

    Returns: 
        data: parsed values
        default: None
    '''

    try:
        for key in keys:
            data = data[key]
        return data
    except (KeyError, IndexError, TypeError):
        return default