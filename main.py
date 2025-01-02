import asyncio
from data_gathering.trustpilot import get_trustpilot_reviews
from API.api_keys import *
from API.proxy_keys import *

reviews_limit  = 5
target_service = "https://www.trustpilot.com/review/tripinsure101.com"

loop = asyncio.get_event_loop()
loop.run_until_complete(get_trustpilot_reviews(target_service, astroproxy_proxy_server, astroproxy_proxy_port, astroproxy_proxy_login, astroproxy_proxy_pass, api_openai, reviews_limit))
loop.close()
print("Trustpilot was completed")