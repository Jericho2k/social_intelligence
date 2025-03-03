import asyncio
import os
from dotenv import load_dotenv
from data_gathering.trustpilot import get_trustpilot_reviews

# Load environment variables
load_dotenv()

reviews_limit = 5
target_service = "https://www.trustpilot.com/review/tripinsure101.com"

# Get environment variables
astroproxy_proxy_server = os.getenv('ASTROPROXY_SERVER')
astroproxy_proxy_port = os.getenv('ASTROPROXY_PORT')
astroproxy_proxy_login = os.getenv('ASTROPROXY_LOGIN')
astroproxy_proxy_pass = os.getenv('ASTROPROXY_PASS')
api_openai = os.getenv('OPENAI_API_KEY')

loop = asyncio.get_event_loop()
loop.run_until_complete(get_trustpilot_reviews(target_service, astroproxy_proxy_server, astroproxy_proxy_port, astroproxy_proxy_login, astroproxy_proxy_pass, api_openai, reviews_limit))
loop.close()

print("Trustpilot was completed")