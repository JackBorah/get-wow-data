import getwowdata as gwd
import requests

search_realm = f'https://us.api.blizzard.com/data/wow/search/connected-realm'

def search(access_token, api , region, namespace, **extra_params):
    """Uses the api's search functionaly for more specific queries.

    Args:
        access_token (str): Returned from get_access_token().
        api (str): The api that will be searched. See searchable apis in README or at https://develop.battle.net/documentation/world-of-warcraft/guides/search.
        region (str): Example: 'us'. Determines which region you'll get data from. See cheatsheet in README or https://develop.battle.net/documentation/guides/regionality-and-apis.
        namespace (str): The namespace being quiried. See more info at https://develop.battle.net/documentation/world-of-warcraft/guides/namespaces.
        **extra_params: A dictionary containing strings like {'realms.slug': 'stormrage'} to refine the search. See search in README or at https://develop.battle.net/documentation/world-of-warcraft/guides/search.

    Returns:
        A json looking dict with nested dicts and/or lists. See README for common usage.
    """
    params = {**{'namespace': namespace, 'access_token':access_token}, **extra_params}
    return requests.get(search_realm, params=params, timeout=10)


access_token = gwd.get_access_token()
x = gwd.search(access_token, 'connected-realm', 'us', 'dynamic-us', **{'realms.slug':'stormrage'})
print(x.url)

x = search(access_token, 'connected-realm', 'us', 'dynamic-us', **{'realms.slug':'stormrage'})
#print(x.json())
print(x.url)