from getwowdata import WowApi
from dotenv import load_dotenv

load_dotenv()

us_api = WowApi('us', 'en_US')
winterhoof_auctions = us_api.get_auctions(4)
