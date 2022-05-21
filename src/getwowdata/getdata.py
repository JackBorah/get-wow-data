"""This module contains functions to query Blizzards World of Warcraft APIs.

Typical usage example:

access_token = get_access_token() 

winterhoof_auctions = get_auctions(access_token, connected_realm_id = 4) 
winterhoof_auctions.json()['auctions']

Copyright (c) 2022 JackBorah
MIT License see LICENSE for more details
"""

import os
import requests
import re

#defaults
region = 'us'
locale = 'en_US'
order_by = 'id'
id_start = 1
page_size = 1000
page = 1
connected_realm_id = 4
profession_id = 164
skill_tier_id = 2477
recipe_id = 1631
item_class_id = 1
item_id = 19019
timeout = 1 #seconds

#urls
urls = {
'access_token': f'https://{region}.battle.net/oauth/token',
'connected_realm_index': f'https://{region}.api.blizzard.com/data/wow/connected-realm/index',
'realm' : f'https://{region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}',
'auction' : f'https://{region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}/auctions',
'profession_index' : f'https://{region}.api.blizzard.com/data/wow/profession/index',
'profession_skill_tier' : f'https://{region}.api.blizzard.com/data/wow/profession/{profession_id}',
'profession_tier_detail' : f'https://{region}.api.blizzard.com/data/wow/profession/{profession_id}/skill-tier/{skill_tier_id}',
'profession_icon' : f'https://{region}.api.blizzard.com/data/wow/media/profession/{profession_id}',
'recipe_detail' : f'https://{region}.api.blizzard.com/data/wow/recipe/{recipe_id}',
'repice_icon' : f'https://{region}.api.blizzard.com/data/wow/media/recipe/{recipe_id}',
'item_classes' : f'https://{region}.api.blizzard.com/data/wow/item-class/index',
'item_subclass' : f'https://{region}.api.blizzard.com/data/wow/item-class/{item_class_id}',
'item_set_index' : f'https://{region}.api.blizzard.com/data/wow/item-set/index?',
'item_icon' : f'https://{region}.api.blizzard.com/data/wow/media/item/{item_id}',
'wow_token' : f'https://{region}.api.blizzard.com/data/wow/token/index',
'search_realm' : f'https://{region}.api.blizzard.com/data/wow/search/connected-realm',
'search_item' : f'https://{region}.api.blizzard.com/data/wow/search/item',
'search_media': f'https://{region}.api.blizzard.com/data/wow/search/media'
}

def get_access_token(region: str, wow_api_id: str = None, wow_api_secret: str = None, timeout: int = 30) -> str:
    """Returns an access token.

    Requires wow_api_id and wow_api_secret to be set as environment variables or
    passed in. Remember not to expose your secret publicly. Each token expires after a day.
    Subsequent get_access_token calls returns the same token until it expires. 

    Args:
        region (str): Example: 'us'. Access tokens will work for all other regions except 'cn' (China).
        wow_api_id (str, optional): Your client id from https://develop.battle.net/. Ignore if id is set as environment variable.
        wow_api_secret (str, optional): Your client secret from https://develop.battle.net/. Ignore if secret is set as environment variable.

    Returns:
        The access token as a string.
    """
    tokenData = {'grant_type': 'client_credentials'}
    try:
        auth = (os.environ["wow_api_id"], os.environ["wow_api_secret"])
        access_token_response = requests.post(urls['access_token'], data=tokenData, auth=auth, timeout=timeout)
        if access_token_response.status_code == requests.codes.ok:
            return  access_token_response.json()['access_token']
    except(KeyError):
        auth = (wow_api_id, wow_api_secret)
        access_token_response = requests.post(urls['access_token'], data=tokenData, auth=auth, timeout=timeout)
        if access_token_response.status_code == requests.codes.ok:
            return  access_token_response.json()['access_token']

def connected_realm_search(access_token: str , region: str, **extra_params: dict) -> dict:
    """Uses the connected realms API's search functionaly for more specific queries.

    Searches can filter by fields returned from the API. Ex: filerting realms by slug == illidan. 
    Below is the data returned from a regular realm query.
    {
        "page": 1,
        "pageSize": 58,
        "maxPageSize": 100,
        "pageCount": 1,
        "results": [
        {
            ...
        },
        "data": {
            "realms": { 
                ...
                "slug":"illidan"
            }
    To only return the realm with the slug == illidan pass {'data.realms.slug':'illidan'} into **extra_params.
    See https://develop.battle.net/documentation/world-of-warcraft/guides/search for more details on search.
    Additional parameters must be sent as a dictionary where keys are str and values are str or int like {'_page': 1, 'realms.slug':'illidan', ...} 

    Args:
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        **extra_params (int/str, optional): Returned data can be filtered by any of its fields. Useful parameters are listed below.
            Ex: {'realm.slug':'illidan'} will only return data with where realm.slug = illidan
        **timeout (int): How long until the request to the API timesout in seconds
        **_pagesize (int, optional): Number of entries in a result page
        **_page (int, optional): The page number that will be returned
        **orderby (str, optional): Accepts a comma seperated field of elements to sort by. See https://develop.battle.net/documentation/world-of-warcraft/guides/search.
        **data.realms.slug (str, optional): Specify the exact name of the realm to to filter by it

    Returns:
       A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    try:
        timeout = extra_params.pop('timeout', 30)
    except(KeyError):
        timeout = 30

    params = {**{'namespace': 'dynamic-us', 'access_token':access_token}, **extra_params}

    response = requests.get(urls['search_realm'], params=params, timeout=timeout)
    print(response.url)
    #return response.json()

def item_search(access_token: str , region: str, **extra_params: dict) -> dict:
    """Uses the items API's search functionality to make more specific queries.

    Ex: Filter by required level and name
    {
    "page": 1,
    "pageSize": 3,
    "maxPageSize": 100,
    "pageCount": 1,
    "results": [
        {
            ...
        },
        "data": {
            "level": 35,
            "required_level": 30,
        ...
            ...
            name.en_US: Garrosh
    Pass {"required_level": 30, "name.en_US: "Garrosh"} into **extra_params
    Additional parameters must be sent as a dictionary where the keys strings and values are strings or ints. 

    Args:
        api (str): The api that will be searched. See searchable apis in README or at https://develop.battle.net/documentation/world-of-warcraft/guides/search.
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        timeout (int): How long until the request to the API timesout in seconds
        **extra_params (int/str, optional): Returned data can be filtered by any of its fields. Useful parameters are listed below.
            Ex: 'data.required_level':35 will only return items where required_level == 35
        **_pagesize (int, optional): Number of entries in a result page
        **_page (int, optional): The page number that will be returned
        **orderby (str, optional): Accepts a comma seperated field of elements to sort by. See https://develop.battle.net/documentation/world-of-warcraft/guides/search.
        **id (int, optional): An items id. Enter in the following format {'id': '(id_start, id_end)'} to specify a set of id's.

    Returns:
       A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    try:
        timeout = extra_params.pop('timeout', 30)
    except(KeyError):
        timeout = 30

    params = {**{'namespace': 'static-us', 'access_token':access_token}, **extra_params}

    response = requests.get(urls['search_item'], params=params, timeout=timeout)
    return response.json()

def get_connected_realms_by_id(connected_realm_id, access_token, region, locale, timeout = 30) -> dict:
    """Gets connected realms by their shared connected_realm_id.

    Args:
        connected_realm_id (int): The connected realm id. Get from connected_realm_index() or from cheatsheets in README.
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['realm'], params={'namespace': f'dynamic-{region}', 'locale': locale, 'access_token':access_token}, timeout=timeout).json() 

def get_auctions(connected_realm_id, access_token, region, locale, timeout = 30) -> dict:
    """Gets all auctions from a realm by its connected_realm_id.

    Args:
        connected_realm_id (int): The connected realm id. Get from connected_realm_index() or from cheatsheets in README.
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['auction'], params={'namespace': f'dynamic-{region}', 'locale':locale, 'access_token':access_token}, timeout=timeout).json()

def get_profession_index(access_token, region, locale, timeout = 30) -> dict:
    """Gets all professions including their names and ids.

    Args:
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['profession_index'], params={'namespace': f'static-{region}', 'locale':locale, 'access_token':access_token}, timeout=timeout).json()

#Includes skill tiers (classic, burning crusade, shadowlands, ...) id
def get_profession_tiers(profession_id, access_token, region, locale, timeout = 30) -> dict:
    """Returns all profession teirs (classic, shadowlands, ...) from a profession by its profession_id.

    Args:
        profession_id (int): The profession's id. Found in get_profession_index() or from cheatsheets in README.
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['profession_skill_tier'], params={'namespace': f'static-{region}', 'locale':locale, 'access_token':access_token}, timeout=timeout).json()

def get_profession_icon(profession_id, access_token, region, locale, timeout = 30) -> dict:
    """Returns a profession's icon. 

    Args:
        profession_id (int): The profession's id. Found in get_profession_index() or from cheatsheets in README.
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['profession_icon'], params={'namespace': f'static-{region}', 'locale':locale, 'access_token':access_token}, timeout=timeout).json()

#Includes the categories (weapon mods, belts, ...) and the recipes (id, name) in them
def get_profession_tier_recipes(profession_id, skill_tier_id, access_token, region, locale, timeout = 30) -> dict:
    """Returns all crafts from a skill teir.

    Args:
        profession_id (int): The profession's id. Found in get_profession_index() or from cheatsheets in README.
        skill_tier_id (int): The skill teir id. Found in get_profession_teirs().
        access_token (str): Returned from get_access_token().
        region (str): Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['profession_tier_detail'], params={'namespace': f'static-{region}', 'locale':locale, 'access_token':access_token}, timeout=timeout).json()

def get_recipe(recipe_id, access_token, region, locale, timeout = 30) -> dict:
    """Returns a recipes details by its id.

    Args:
        recipe_id (int): The recipe's id. Found in get_profession_tier_details().
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['recipe_detail'], params={'namespace': f'static-{region}', 'locale':locale, 'access_token':access_token}, timeout=timeout).json()

def get_recipe_icon(recipe_id, access_token, region, locale, timeout = 30) -> dict:
    """Returns a recipes icon.

    Args:
        recipe_id (int): The recipe's id. Found in get_profession_tier_details().
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['repice_icon'], params={'namespace': f'static-{region}', 'locale':locale, 'access_token':access_token}, timeout=timeout).json()

def get_item_classes(access_token, region, locale, timeout = 30) -> dict:
    """Returns all item classes (consumable, container, weapon, ...).

    Args:
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['item_classes'], params={'namespace': f'static-{region}', 'locale':locale, 'access_token':access_token}, timeout=timeout).json()

#flasks, vantus runes, ...
def get_item_subclasses(item_class_id, access_token, region, locale, timeout = 30) -> dict:
    """Returns all item subclasses (class: consumable, subclass: potion, elixir, ...).

    Args:
        item_class_id (int): Item class id. Found with get_item_classes().
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['item_subclass'], params={'namespace': f'static-{region}', 'locale':locale, 'access_token':access_token}, timeout=timeout).json()

def get_item_set_index(access_token, region, locale, timeout = 30) -> dict:
    """Returns all item sets. Ex: teir sets

    Args:
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['item_set_index'], params={'namespace': f'static-{region}', 'locale':locale,'access_token':access_token}, timeout=timeout).json()

def get_item_icon(item_id, access_token, region, locale, timeout = 30) -> dict:
    """Returns the icon for an item.

    Args:
        item_id (int): The items id. Get from search() with api = item.
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['item_icon'], params={'namespace':f'static-{region}', 'locale':locale,'access_token':access_token}, timeout=timeout).json()

def get_wow_token(access_token, region, locale, timeout = 30) -> dict:
    """Returns the price of the wow token and the timestamp of its last update.

    Args:
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    return requests.get(urls['wow_token'], params={'namespace':f'dynamic-{region}', 'locale':locale, 'access_token':access_token}, timeout=timeout).json()

def get_connected_realm_index(access_token, region, locale, timeout = 30) -> dict:
    """Returns a dict where {key = Realm name: value = connected realm id}

    Args:
        access_token (str): Returned from get_access_token().
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        locale (str): The language that a resource will be returned in. If Null all translations will be returned. See https://develop.battle.net/documentation/world-of-warcraft/guides/localization
        timeout (int): How long until the request to the API timesout in seconds.

    Returns:
        A dict where {realm_name: connected_realm_id}
    """

    index = {}
    id_pattern = re.compile('[\d]+')
    
    response_index = connected_realm_search(access_token, 'us').json
    for realms in response_index["connected_realms"]:
        realms_response = requests.get(realms['href'], params={'access_token':access_token, 'locale':locale}).json()

        for realm in realms_response['realms']:
            connected_realm_id = id_pattern.search(realm['connected_realm']['href'])
            index[realm['name']] = connected_realm_id.group()
    
    return index
