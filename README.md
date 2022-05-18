# getwowdata

**getwowdata** makes it easier to pull data from Blizzard's World of Warcraft (WoW) API's.

```python
import getwowdata

#Don't publish your secret key! Set it as an environment variable (see setup)
#Or for private use set the variables below in your script
wow_api_id = #your client id
wow_api_secret = #your client secret
access_token = get_access_token() #

winterhoof_auctions = get_auctions(4) #4 is the connected-realm id for the winterhoof server
winterhoof_auctions.json()['auctions'][0] #.json() pythonifies json into dictionaries and lists
```



## Table of Contents
- [Installing](#Installing)
- [Features](#Features)
- [Setup](#Setup)
- [How to use](#How-to-use)
- [Cheatsheet](#Cheatsheet)
- [Feedback](#Feedback)
- [License](#License)

## Installing
Getwowdata is avilable on PyPi:
```console
$ python -m pip install getwowdata
```
## Features
Currently only a subset of the available APIs can be pulled from.
- get an access token
- realms and connected realms APIs
- profession APIs
- item APIs
- auction house API
- wow token API

## Setup
1. Go to [https://develop.battle.net/](https://develop.battle.net/) (This is an official Blizzard website)
2. Click on Get started and login. 
3. Now click create client and fill out the form.

Now check out [How to use](#how-to-use) to see how you can use your Client Id and Client Secret to make requests to Blizzard's APIs.

Remember not to commit your wow_api_secret! You can set wow_api_id and wow_api_secret as environment variables and **getwowdata** will read these credentials from there.
## How to use
```python
stub
```
The href's in the json are links to related elements.


#### Reading json
Using a normal print() on response.json() outputs gibberish.
I recommend either the pprint module or viewing the json from [this list](https://develop.battle.net/documentation/world-of-warcraft/game-data-apis) of all the available APIs.


#### Item bonus list
The items with a bonus_list can either be found on wowhead or found in an opaque wow tools query. Blizzard does not make this available through an api. The wowhead page for an item does take a querystring with a bonusId which will return the correct variant of the item.

I will make some solution for this even if its just another cheatsheet with a list of bonus id's and their effects. 
## Parameter Cheatsheet

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
I was writing this for [my WoW profession profit calculator](https://github.com/JackBorah/wow-profit-calculator) site and thought that other people could find this useful.

Hopefully you'll find this useful!