import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import tweepy
import config
import auth
import datetime
import logging


# Create API object
api = api_socket = auth.authenticateConfig()

""" TODO: 
    Create Event Search Object to store the list of search parameters and logic to create Query String
    """
query = "SenzoMeyiwatrial"  
date_since = '2022-11-15'
date_until ='2022-11-17'

tweets = [tweet for tweet in tweepy.Cursor(api.search_tweets, q=query, lang="en", wait_on_rate_limit=True,
                                           since=date_since, until=date_until, tweet_mode='extended').items(100)]
""" _summary_ : 
    Tweets returned from the Twitter API are stored in a list of Tweet objects.
"""

df = pd.DataFrame(columns=['created_at', 'id', 'id_str', 'text', 'truncated',
                  'entities', 'metadata', 'source', 'likes', 'retweets', 'user'])
""" 
    Dataframe For Tweets, columns are the attributes of the tweet object
"""


tweets.sort(key=lambda x: x.created_at, reverse=True)


for tweet in tweets:
    """_summary_ : 
    Get the values for each tweet, and append them to the dataframe
    """
    created_at = tweet.created_at 
    id = tweet.id
    id_str = tweet.id_str
    truncated = tweet.truncated
    entities = tweet.entities
    metadata = tweet.metadata
    source = tweet.source
    likes = tweet.favorite_count
    retweets = tweet.retweet_count
    user = tweet.user.screen_name

    """
    Special case for retweets :
    """
    try:
        text = tweet.retweeted_status.full_text
    except AttributeError as e:
        logging.error("AttributeError - %s", str(e))
        text = "tweet.full_text" # Is this supposed to be a string or a variable?

    df = df.append({'created_at': created_at, 'id': id, 'id_str': id_str,
                    'text': text, 'truncated': truncated, 'entities': entities,
                    'metadata': metadata, 'source': source, 'likes': likes,
                    'retweets': retweets, 'user': user
                    }, ignore_index=True)
    print(user)
filename = 'tweets.csv'
df.to_csv(filename)

