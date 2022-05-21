# getwowdata

**getwowdata** already implements requests to the World of Warcraft (WoW) APIs so you don't have to.

Example: Get the value of all auctions on Winterhoof.
```python
import getwowdata as gwd

#optional
wow_api_id = #your client id
wow_api_secret = #your client secret

total_value = 0

access_token = gwd.get_access_token()

winterhoof_auctions = gwd.get_auctions(access_token, connected_realm_id = 4) #4 is the connected-realm id for the winterhoof server
winterhoof_auctions = winterhoof_auctions.json() #.json() pythonifies json into dictionaries and lists

for item in winterhoof_auctions['auctions']:
    try:
        total_value += item['unit_price']
    except(KeyError):
        total_value += item['buyout']


print(gwd.as_gold(total_value))
#430,423,357g 07s 00c
```



## Table of Contents
- [Features](#Features)
- [Installing](#Installing)
- [Setup](#Setup)
- [API](#API)
- [Notes on the data](#Notes-on-the-data)
- [Cheatsheet](#Cheatsheet)
- [Feedback](#Feedback)
- [License](#License)

## Features
Currently only a subset of the available APIs can be pulled from.
- search a bunch of APIs
- get an access token
- get realms and connected realms APIs
- get profession APIs
- get item APIs
- get auction house API
- get wow token API

## Installing
Getwowdata is avilable on PyPi:
```console
$ python -m pip install getwowdata
```
## Setup
You consume any blizzard API you need a Client Id and Client Secret.
1. Go to [https://develop.battle.net/](https://develop.battle.net/)
2. Click on Get started and login. 
3. Now click create client and fill out the form.
4. Finally, you have a Client Id and Client Secret to query Blizzards APIs

#### Setting the Secret and Id as an environment variable
##### Windows
1. Click on the start button
2. Type environment variables
3. Click Edit system environment variables
4. Click Environment Variables...
5. Click either New... buttons 
6. set the name to wow_api_id or wow_api_secret and their respective values

**Remember not to commit your wow_api_secret!** You can set wow_api_id and wow_api_secret as environment variables and **getwowdata** will read these credentials from there.

## API
There are two ways to consume the World of Warcraft API the search or get functions. 

#### Search


Example: Searching for a specific server by name
```Python
import getwowdata as gwd

access_token = gwd.get_access_token()
gwd.search(access_token, 'connected-realm', 'realms.slug': 'illidan')
```

- 'realms.slug': 'realm-name'
- 'realms.timezone
##### Searchable API strings
- azerite-essence 
- connected-realm
    - Use to search for a realm/realms.
- realm
    - Use to search for a realm/realms
- creature
    - Search for creatures like wolves, clefthoofs, ...
- item
- journal-encounter
    - Quests
- media
    - all icons
- mount
- spell

#### Gets
```python
get_connected_realm_index()
```
Realms that are connected share a single connected realm id. This returns a list of those id's and a link to their associated realms.
```python
get_realm()
```
```python
get_auctions()
```
```python
get_profession_index()
```
```python
get_profession_tiers()
```
```python
get_profession_icon()
```
```python
get_profession_tier_details()
```
```python
get_recipe_details()
```
```python
get_recipe_icon()
```
```python
get_item_classes()
```
```python
get_item_subclasses()
```
```python
get_item_set_index()
```
```python
get_item_list()
```
```python
get_item_icon()
```
```python
get_wow_token()
```

#### Reading json
Using a normal print() on response.json() outputs gibberish.
I recommend either the pprint module or viewing the json from [this list](https://develop.battle.net/documentation/world-of-warcraft/game-data-apis) of all the available APIs.

This package is built with [requests](https://docs.python-requests.org/en/latest/) so methods like .json(), .text, .url, etc. all work with the results of get_x(). See [requests](https://docs.python-requests.org/en/latest/) for more info on what you can do. 

## Notes on the data
#### Href's
The href's in the json are links to related elements. The first link in a query is the url which made the query.
#### Prices
The prices or value of an item is in the following format gggg*sscc, where g = gold, s = silver, c = copper. 
Silver and copper are fixed in the last 4 decimal spaces whlie gold can be as any number of spaces before silver. So 25289400 is 2528g 94s 00c.

#### buyout vs unit_price
Stackable items have a single unit_price while unique items like weapons have a bid/buyout price.

#### Item bonus list
The item bonus list are the modifiers applied to an item.
Versions of an item with different bonuses can be found on [wowhead](https://www.wowhead.com/). Blizzard does not make the bonus values and their corresponding effects available through an api. The wowhead page for an item shows its bonuses (if selected under item versions) take a querystring with a bonusId which will return the correct variant of the item.

I will make some solution for this even if its just another cheatsheet with a list of bonus id's and their effects. 
#### Item context
Where the item was created. Incomplete list
| Context 	| Value          	|
|---------	|----------------	|
| 1       	| Normal Dungeon 	|
| 5       	| Heroic Raid    	|
| 11      	| Quest Reward   	|
| 14      	| Vendor         	|
| 15      	| Black Market   	|
#### Item modifiers
Stub
####
## Parameter Cheatsheet
Incomplete list
| Region 	| Namespace        	| locale (language) 	|
|--------	|------------------	|-------------------	|
| us     	| static-{region}  	| en_US             	|
| eu     	| dynamic-{region} 	| es_MX             	|
| kr     	| profile-{region} 	| pt_BR             	|
| tw     	|                  	| de_DE             	|
| cn     	|                  	| en_GB             	|
|        	|                  	| es_ES             	|
|        	|                  	| fr_FR             	|
|        	|                  	| it_IT             	|
|        	|                  	| ru_RU             	|
|        	|                  	| ko_KR             	|
|        	|                  	| zh_TW             	|
|        	|                  	| zh_CN             	|


## Feedback
Feel free to [file an issue](https://github.com/JackBorah/getwowdata/issues/new).
I'm currently learning how to code so if you have any suggestions or corrections I would really appriciate it.


## License
MIT

## Related project
I was writing this for [my WoW profession profit calculator](https://github.com/JackBorah/wow-profit-calculator) site.

Hopefully you'll find this useful!