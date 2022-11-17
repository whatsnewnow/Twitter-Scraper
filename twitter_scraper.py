import pandas as pd
import tweepy
import config 
import auth
import datetime
import logging

# function should return a list of tweets, in order of most recent, that match the query.
def search_by_keyword(api, date_since='2022-10-14', date_until=datetime.datetime.now().date(), query="kanye", max_tweets=10):
    df = pd.DataFrame(columns=['created_at', 'id', 'id_str', 'text', 'truncated', 'entities', 'metadata', 'source', 'likes', 'retweets', 'user'])
    try:
        tweets = tweepy.Cursor(api.search_tweets, q=query, lang='en', since=date_since, until=date_until, tweet_mode="extended", wait_on_rate_limit=True,wait_on_rate_limit_notify=True ).items(int(max_tweets))
    except tweepy.TweepError as e:
        logging.error(e)
        print(e)

    tweets = tweepy.Cursor(api.search_tweets, q=query, lang="en", wait_on_rate_limit=True, since=date_since, until=date_until, tweet_mode='extended').items(10)
    
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
    # Create API object
    api_socket = auth.authenticateConfig()   

    # search by keyword
    query = input("Please input search query: ")

    hours_since = int(input("Please input the number of hours ago you'd like to search: "))
    max_tweets = input("Please input the maximum number of tweets you'd like to returned: ")
    
    date_since = hours_ago_to_datetime(hours_since)
    
    date_since = date_since.date()
    print(date_since)
    search_by_keyword(api=api_socket,date_since= date_since,query= query, max_tweets=max_tweets)
    

def hours_ago_to_datetime(hours_ago):
    if int(hours_ago)>=24:
        days_ago = int(hours_ago)/24
        days_ago = int(days_ago)
        hours_ago = int(hours_ago) - (days_ago%24)
        date_since = datetime.datetime.now() - datetime.timedelta(days=days_ago, hours=hours_ago)
       
    return datetime.datetime.now() - datetime.timedelta(hours=hours_ago)

     

# If this script file's name is main, run the main function.
if __name__ == "__main__": 
    main()