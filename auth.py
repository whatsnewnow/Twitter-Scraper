from fileinput import filename
from threading import TIMEOUT_MAX
import tweepy
import config
import signal
import logging

# Authenticate the config file's API credentials
def authenticateConfig(): 
    logging.basicConfig(filename='sys.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

    # Authenticate to Twitter    
    try: 
        auth = tweepy.OAuthHandler(config.CONSUMER_KEY, config.CONSUMER_SECRET_KEY)
        auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth, wait_on_rate_limit=True, timeout=30) # Setting these properties true will make the api to automatically wait for rate limits to replenish

        logging.info("Authentication successful")

        return api # Return the api object to caller
    except tweepy.HTTPException as e:
        logging.error("Authentication failed - %s", str(e))
        return None # Return None to caller (TODO: add error handling)
    
    
    
if __name__ == "__main__":
    authenticateConfig()