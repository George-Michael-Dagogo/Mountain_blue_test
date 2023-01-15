
today = datetime.date.today()
tomorrow = datetime.date.today() - datetime.timedelta(days=-1)
now = datetime.datetime.now()
current_time = now.strftime("%H:%M")
api_key = os.environ["API_KEY"]
api_key_secret = os.environ["API_KEY_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]
auth = tweepy.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)
print('# Daily pipeline status')

keywords = ['Buhari OR APC OR  PeterObi OR Tinubu OR PDP OR Atiku OR LabourParty']
#keywords = ['Buhari','APC', 'PeterObi','Tinubu','Atiku']
#it seems the api does not return every tweet containing at least one or every keyword, it returns the only tweets that contains every keyword
#solution was to use the OR in the keywords string as this is for tweets search only and might give errors in pure python
limit = 10000

tweets = tweepy.Cursor(api.search_tweets, q = keywords,count = 200, tweet_mode = 'extended',geocode='9.0820,8.6753,450mi', until=today).items(limit)

columns = ['time_created', 'screen_name','name', 'tweet','loca_tion', 'descrip_tion','verified','followers', 'source','geo_enabled','retweet_count','truncated','lang','likes']
data = []


for tweet in tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.user.name,tweet.full_text, tweet.user.location, tweet.user.description,tweet.user.verified,tweet.user.followers_count,tweet.source,tweet.user.geo_enabled,tweet.retweet_count,tweet.truncated,tweet.lang,tweet.favorite_count])
    
df = pd.DataFrame(data , columns=columns)
df = df[~df.tweet.str.contains("RT")]
#removes retweeted tweets
df = df.reset_index(drop = True)
print('##',len(df), 'new rows of data was successfully extracted from Twitter API and preview below')
print('##', df.head())
