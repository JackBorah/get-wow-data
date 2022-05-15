import os
import requests
from pprint import pprint

#defaults
region = 'us'
dynamic_namespace = 'dynamic-us'
static_namespace = 'static-us'
locale = 'en_US'
order_by = 'id'
id_start = 1
page_size = 1000
page = 1
connected_realm_id = 4
profession_id = 1
skill_tier_id = 1
recipe_id = 1
item_class_id = 1
item_id = 1
timeout = 1

#urls
access_token_url = f'https://{region}.battle.net/oauth/token'
connected_realm_index_url = f'https://{region}.api.blizzard.com/data/wow/connected-realm/index'
realm_url = f'https://{region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}'
auction_url = f'https://{region}.api.blizzard.com/data/wow/connected-realm/{connected_realm_id}/auctions'
profession_index_url = f'https://{region}.api.blizzard.com/data/wow/profession/index'
profession_skill_teir_url = f'https://{region}.api.blizzard.com/data/wow/profession/{profession_id}'
profession_teir_detail_url = f'https://{region}.api.blizzard.com/data/wow/profession/{profession_id}/skill-tier/{skill_tier_id}'
profession_icon_url = f'https://{region}.api.blizzard.com/data/wow/media/profession/{profession_id}'
recipe_detail_url = f'https://{region}.api.blizzard.com/data/wow/recipe/{recipe_id}'
repice_icon_url = f'https://{region}.api.blizzard.com/data/wow/media/recipe/{recipe_id}'
item_classes_url = f'https://{region}.api.blizzard.com/data/wow/item-class/index'
item_subclass_url = f'https://{region}.api.blizzard.com/data/wow/item-class/{item_class_id}'
item_set_index_url = f'https://{region}.api.blizzard.com/data/wow/item-set/index?'
item_list_url = f'https://{region}.api.blizzard.com/data/wow/search/item'
item_icon_url = f'https://{region}.api.blizzard.com/data/wow/media/item/{item_id}'
wow_token_url = f'https://{region}.api.blizzard.com/data/wow/token/index'

#token data
tokenData = {'grant_type': 'client_credentials'}

#Client ID, secret
auth = (os.environ["wowApiId"], os.environ["wowApiSecret"])

def get_access_token(region = region, tokenData = tokenData, auth = auth):
    return requests.post(access_token_url, data=tokenData, auth=auth, timeout=timeout)
    
access_token = get_access_token()['access_token']

def get_connected_realm_index(region = region, namespace = dynamic_namespace, locale = locale):
    return requests.get(connected_realm_index_url, params={'namespace': namespace, 'locale': locale, 'access_token':access_token}, timeout=timeout)

def get_realm(connected_realm_id = connected_realm_id, region = region, namespace = dynamic_namespace, locale = locale):
    return requests.get(realm_url, params={'namespace': namespace, 'locale': locale, 'access_token':access_token}, timeout=timeout)

def get_auctions(connected_realm_id = connected_realm_id, region = region, namespace = dynamic_namespace, locale = locale):
    return requests.get(auction_url, params={'namespace':namespace, 'locale':locale, 'access_token':access_token}, timeout=timeout)

def get_profession_index(region = region, namespace = static_namespace, locale = locale):
    return requests.get(profession_index_url, params={'namespace':namespace, 'locale':locale, 'access_token':access_token}, timeout=timeout)

#Includes skill teirs (classic, burning crusade, shadowlands, ...) id
def get_profession_teirs(profession_id = profession_id, region = region, namespace = static_namespace, locale = locale):
    return requests.get(profession_skill_teir_url, params={'namespace':namespace, 'locale':locale, 'access_token':access_token}, timeout=timeout)

def get_profession_icon(profession_id = profession_id, region = region, namespace = static_namespace, locale = locale):
    return requests.get(profession_icon_url, params={'namespace':namespace, 'locale':locale, 'access_token':access_token}, timeout=timeout)

#Includes the categories (weapon mods, belts, ...) and the recipes (id, name) in them
def get_profession_teir_details(profession_id = profession_id, skill_tier_id = skill_tier_id, region = region, namespace = static_namespace, locale = locale):
    return requests.get(profession_teir_detail_url, params={'namespace':namespace, 'locale':locale, 'access_token':access_token}, timeout=timeout)

def get_recipe_details(recipe_id = recipe_id, region = region, namespace = static_namespace, locale = locale):
    return requests.get(recipe_detail_url, params={'namespace':namespace, 'locale':locale, 'access_token':access_token}, timeout=timeout)

def get_recipe_icon(recipe_id = recipe_id, region = region, namespace = static_namespace, locale = locale):
    return requests.get(repice_icon_url, params={'namespace':namespace, 'locale':locale, 'access_token':access_token}, timeout=timeout)

#consumable, ...
def get_item_classes(region = region, namespace = static_namespace, locale = locale):
    return requests.get(item_classes_url, params={'namespace':namespace, 'locale':locale, 'access_token':access_token}, timeout=timeout)

#flasks, vantus runes, ...
def get_item_subclasses(item_class_id = item_class_id, region = region, namespace = static_namespace, locale = locale):
    return requests.get(item_subclass_url, params={'namespace':namespace, 'locale':locale, 'access_token':access_token}, timeout=timeout)

def get_item_set_index(region = region, namespace = static_namespace, locale = locale):
    return requests.get(item_set_index_url, params={'namespace':namespace, 'locale':locale,'access_token':access_token}, timeout=timeout)

def get_item_list(id_start = id_start, page_size = page_size, page = page, order_by = order_by, region = region, namespace = static_namespace):
    return requests.get(item_list_url, params={'namespace':namespace, '_pageSize': page_size,'_page':page, 'orderby': order_by, 'id':f'[{id_start},]', 'access_token':access_token}, timeout=timeout)

def get_item_icon(item_id = item_id, region = region, namespace = static_namespace, locale = locale):
    return requests.get(item_icon_url, params={'namespace':namespace, 'locale':locale,'access_token':access_token}, timeout=timeout)

def get_wow_token(region = region, namespace = static_namespace, locale = locale):
    return requests.get(wow_token_url, params={'namespace':namespace, 'locale':locale, 'access_token':access_token}, timeout=timeout)