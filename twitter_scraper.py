import pandas as pd
import tweepy
import api_keys 

# Authenticate to Twitter
# This authentication approach isn't sustainable, temporarily solution for testing. 
# Transfer to OAuth2 and configparser for production.

def auth():
    try: 
        auth = tweepy.OAuthHandler(api_keys.CLIENT_KEY, api_keys.CLIENT_SECRET_KEY)
        auth.set_access_token(api_keys.ACCESS_TOKEN, api_keys.ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
    except:
        print("Error: Authentication Failed")
        
def main():
    auth()    

# If this script file's name is main, run the main function.
if __name__ == "__main__": 
    main()