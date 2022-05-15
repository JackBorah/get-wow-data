gets the same access token across multiple requests
each access token lasts a day
use pprint from import pprint to print out legible json
illidanAH.json()['auctions'][0] will get the first auction from the illidanAH
links.self.href is the link from where the current json response came from

its annoying but the items with a bonus_list can either be found on wowhead or found in an opaque wow tools query.
I don't think either of these could be fully automated like pulling data if only they supplied it from the api 
This seems like I ahve to update it by hand.
the wowhead page for an item does take a querystring with a bonusId which will return the correct variant of the item

Provides functions that make requests to specific World of Warcraft API's. 