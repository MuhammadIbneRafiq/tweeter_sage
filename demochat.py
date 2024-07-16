from ntscraper import Nitter
import pandas as pd 

scraper = Nitter(0)

tweets = scraper.get_tweets("buildspace", mode = 'hashtag', number=10)
final_tweets = []
for x in tweets['tweets']:
    data = [x['link'], x['text'],x['date'],x['stats']['likes'],x['stats']['comments']]
    final_tweets.append(data)
    
dat = pd.DataFrame(final_tweets, columns =['twitter_link','text','date','likes','comments'])

print(dat)


tweets = scraper.get_profile_info("JeffBezos")

print(tweets)

def get_tweets(name, modes, no):
    tweets = scraper.get_tweets(name, mode = modes, number=no)
    final_tweets = []
    for x in tweets['tweets']:
        data = [x['link'], x['text'],x['date'],x['stats']['likes'],x['stats']['comments']]
        final_tweets.append(data)
    dat= pd.DataFrame(final_tweets, columns =['twitter_link','text','date','likes','comments'])
    return dat

data = get_tweets('JeffBezos','user',6)
print('yo check this is what will be displayed instead of AI messages maybe', data)

print('the profile belongs to this guys', scraper.get_profile_info('BillGates'))