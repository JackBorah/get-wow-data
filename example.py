"""All examples found in documentation are found below."""

#auction example
from dotenv import load_dotenv
import getwowdata as gwd


#get wow_api_id and wow_api_secret from .env
#or pass as kwargs into WowApi()
load_dotenv()

total_value = 0

us_api = gwd.WowApi('us', 'en_US') #region, language (optional)
winterhoof_auctions = us_api.get_auctions(4) #4 == Winterhoof's connected realm id

for item in winterhoof_auctions['auctions']:
    if item.get('unit_price'):
        total_value += item.get('unit_price')
    elif item.get('buyout'):
        total_value += item.get('buyout')
    elif item.get('bid'):
        total_value += item.get('bid')

print(gwd.as_gold(total_value))
#prints 430,846,968g 67s 00c

#item_search example
from pprint import pprint
from dotenv import load_dotenv
from getwowdata import WowApi

load_dotenv()

eu_api = WowApi('eu', 'en_US')
params = {"quality.name.en_US":"Legendary", "name.en_US":"Thunderfury, Blessed"}

result_item = eu_api.item_search(**params)
pprint(result_item)

#get_wow_token example
from pprint import pprint
from dotenv import load_dotenv
from getwowdata import WowApi

load_dotenv()

us_api = WowApi('us', 'en_US')
wow_token_data = us_api.get_wow_token()

pprint(wow_token_data)
#prints:
# {'_links': {'self': {'href': 'https://us.api.blizzard.com/data/wow/token/?namespace=dynamic-us'}},
# 'last_updated_timestamp': 1653847530000,
# 'price': 1656890000} 