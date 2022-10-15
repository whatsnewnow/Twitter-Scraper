import pandas as pd
import tweepy
import config 
import auth
import logging

# function should return a list of tweets, in order of most recent, that match the query.
def search_by_keyword(api, date_since, date_until, words):
    df = pd.DataFrame(columns=['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'metadata', 'source', 'likes', 'retweets', 'user'])
    
    tweets = tweepy.Cursor(api.search_tweets, q=words, lang='en', since=date_since, until=date_until, tweet_mode="extended").items(100)
    
    #tweets = tweepy.Cursor(api.search_tweets, q=words, lang="en", wait_on_rate_limit=True, since=date_since, until=date_until, tweet_mode='extended').items(10)
    
    list_tweets = [tweet for tweet in tweets] # loop through each tweet returned and add to list
    
    for tweet in list_tweets:
        # get the values for each tweet
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
        
        # get the full text of the tweet, special case for retweets
        try: 
            text = tweet.retweeted_status.full_text
        except AttributeError as e:
            logging.error("AttributeError - %s", str(e))
            text = "tweet.full_text"
            
        # append each tweet's values to dataframe
        df = df.append({'created_at': created_at, 'id': id, 'id_str': id_str,
                        'text': text, 'truncated': truncated, 'entities': entities,
                        'metadata': metadata, 'source': source, 'likes': likes, 
                        'retweets': retweets, 'user': user
                        }, ignore_index=True)
    
    filename = 'tweets.csv'
    df.to_csv(filename)



        
def main():
    api_socket = auth.authenticateConfig()   
    
    query = "kanye"
    date_since = '2022-10-10'
    date_until = '2022-10-14'
    
    search_by_keyword(api_socket, date_since, date_until, query)
    

    

     

# If this script file's name is main, run the main function.
if __name__ == "__main__": 
    main()