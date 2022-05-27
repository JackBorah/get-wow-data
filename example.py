import getwowdata as gwd
from dotenv import load_dotenv

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


from getwowdata import WowApi

eu_api = WowApi('eu', 'en_US')
params = {"id":19019}

result_item = eu_api.item_search(**params)
print(result_item['results'][0]['data']['name']['en_US'])
