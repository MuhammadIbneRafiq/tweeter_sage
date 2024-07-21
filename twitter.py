import tweepy
from dotenv import load_dotenv
import os

load_dotenv()
BEAERER_TOKEN = os.getenv('BEARER_TOKEN')


client = tweepy.Client(bearer_token=BEAERER_TOKEN)


query = 'hiring ui/ux designer -is:retweet'

response = client.search_recent_tweets(query=query, max_results=10, tweet_fields=['created_at', 'lang'], expansions=['author_id'])

users = {u['id']: u for u in response.includes['users']}

for tweet in response.data:
    print(tweet.id)
    print(tweet.lang)


import tweepy
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Twitter API credentials from environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

if not all([CLIENT_ID, CLIENT_SECRET]):
    print("CLIENT_ID or CLIENT_SECRET is not set. Please check your .env file.")
    exit(1)

# OAuth 2.0 Bearer Token
auth = tweepy.OAuth2BearerHandler(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

# Instantiate the tweepy API
client = tweepy.Client(auth)

search_query = "'ref' 'world cup' -is:retweet -is:reply -has:links"
no_of_tweets = 100

try:
    # The number of tweets we want to retrieve from the search
    tweets = client.search_recent_tweets(query=search_query, 
                                         tweet_fields=['created_at', 'public_metrics', 'source'], 
                                         max_results=no_of_tweets)

    # Pulling some attributes from the tweet
    attributes_container = [[tweet.user.username, tweet.created_at, tweet.public_metrics['like_count'], tweet.source, tweet.text] for tweet in tweets.data]

    # Creation of column list to rename the columns in the dataframe
    columns = ["User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet"]

    # Creation of DataFrame
    tweets_df = pd.DataFrame(attributes_container, columns=columns)
    
    # Display the DataFrame
    print(tweets_df)

except tweepy.TweepyException as e:
    print('Status Failed On,', str(e))
except Exception as e:
    print('An unexpected error occurred:', str(e))