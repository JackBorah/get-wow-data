import getwowdata as gwd
from pprint import pprint

total_value = 0

access_token = gwd.get_access_token()

winterhoof_auctions = gwd.get_auctions(access_token, connected_realm_id = 4) #4 is the connected-realm id for the winterhoof server
winterhoof_auctions = winterhoof_auctions.json() #.json() pythonifies json into dictionaries and lists
#pprint(winterhoof_auctions['auctions'][0]) #pprint prints json in a legible format
for item in winterhoof_auctions['auctions']:
    try:
        total_value += item['unit_price']
    except(KeyError):
        total_value += item['buyout']


print(total_value)