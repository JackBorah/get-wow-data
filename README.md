# getwowdata

**getwowdata** implements requests to the World of Warcraft (WoW) APIs so you don't have to.

Example: Get the value of all auctions from the Winterhoof server.
```python
import getwowdata as gwd
from dotenv import load_dotenv

#get wow_api_id and wow_api_secret from .env
#or pass as kwargs into WowApi()
load_dotenv()

total_value = 0

us_api = gwd.WowApi('us', 'en_US')
winterhoof_auctions = us_api.get_auctions(4)

for item in winterhoof_auctions['auctions']:
    try:
        total_value += item['unit_price']
    except KeyError:
        total_value += item['buyout']

print(gwd.as_gold(total_value))
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
Supported APIs (see [this](https://develop.battle.net/documentation/world-of-warcraft/game-data-apis) for a complete list of APIs provided by blizzard)
- Connected Realms
- Items
    - Icons
- Auctions
- Professions
    - Recipes
    - Icons
- Wow Token


## Installing
Getwowdata is avilable on PyPi:
```console
$ python -m pip install getwowdata
```
## Setup
To access any blizzard API you need a Client Id and Client Secret.
1. Go to [https://develop.battle.net/](https://develop.battle.net/)
2. Click on Get started and login. 
3. Now click create client and fill out the form.
4. You now have a Client Id and Client Secret to query Blizzards APIs

*Remember not to commit your wow_api_secret!* You can set wow_api_id and wow_api_secret as environment variables and **getwowdata** will read these credentials from there.
#### Setting the id and secret as an environment variable
1. Install dotenv with pip
```
python -m pip install dotenv
```
2. Create a file called .env
3. Set wow_api_id andwow_api_secret
```
wow_api_id = x
wow_api_secret = y
```
4. To load environment variables from .env
```python
from dotenv import load_dotenv
load_dotenv()
```

## API
There are two ways to consume the World of Warcraft API the search or get functions. 

#### Search


Example: Searching for thunderfury by its id and printing its name. 
```Python
from getwowdata import WowApi

eu_api = WowApi('eu', 'en_US')
params = {"id":19019}

result_item = eu_api.item_search(**params)
print(result_item['results'][0]['data']['name']['en_US'])
```
#### Searches STUB

Wow_Api.connected_realm_search()
Wow_Api.item_search()

#### Gets STUB

Wow_Api.get_connected_realm_index()
Wow_Api.get_realm()
Wow_Api.get_auctions()
Wow_Api.get_profession_index()
Wow_Api.get_profession_tiers()
Wow_Api.get_profession_icon()
Wow_Api.get_profession_tier_details()
Wow_Api.get_recipe_details()
Wow_Api.get_recipe_icon()
Wow_Api.get_item_classes()
Wow_Api.get_item_subclasses()
Wow_Api.get_item_set_index()
Wow_Api.get_item_list()
Wow_Api.get_item_icon()
Wow_Api.get_wow_token()

#### Reading json
Using a normal print() on response.json() outputs gibberish.
I recommend either the pprint module or viewing the json from [this list](https://develop.battle.net/documentation/world-of-warcraft/game-data-apis) of all the available APIs. 

## Notes on the data
Visit [https://develop.battle.net/documentation/world-of-warcraft](https://develop.battle.net/documentation/world-of-warcraft) for blizzard official documentation.
Below are notes that i've gathered from the documentation, reading the returned data, and
from forum posts/reddit. 
#### Href's
The href's in the json are links to related elements. One of the links will be to the url that produced that data. 
#### Prices
The prices or value of an item is in the following format g*sscc, where g = gold, s = silver, c = copper. 
Silver and copper are fixed in the last 4 decimal spaces whlie gold can be as any number of spaces before silver. So 25289400 is 2528g 94s 00c.

#### buyout vs unit_price
Stackable items have a single unit_price while unique items like weapons have a bid/buyout price.

#### Item bonus list
The item bonus list are the modifiers applied to an item, such as the level its scaled to. Blizzard does not make the bonus values and their corresponding effects available through an API. 

Versions of an item with different bonuses can be found on [wowhead](https://www.wowhead.com/). Mouse over select version and pick your desired version from the drop down menu. 

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

I'm currently teaching myself how to code, so, if you have any suggestions or corrections I would really appriciate it.


## License
MIT

## Related project
I was writing this for [my WoW profession profit calculator](https://github.com/JackBorah/wow-profit-calculator) site.

Hopefully you'll find this useful!