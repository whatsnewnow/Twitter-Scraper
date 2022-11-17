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
        auth = tweepy.OAuthHandler(config.api_key, config.api_key_secret)
        auth.set_access_token(config.access_token, config.access_token_secret)

        api = tweepy.API(auth, wait_on_rate_limit=True, timeout=30) # Setting these properties true will make the api to automatically wait for rate limits to replenish

        logging.info("Authentication successful")

        return api # Return the api object to caller
    except tweepy.HTTPException as e:
        logging.error("Authentication failed - %s", str(e))
        return None # Return None to caller (TODO: add error handling)
    
    
    
if __name__ == "__main__":
    authenticateConfig()