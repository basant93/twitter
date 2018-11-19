import json
import redis
from collections import defaultdict
from collections import Counter 
import tweepy



class TweetStore:

    # Redis Configuration
    redis_host = "localhost"
    redis_port = 6379
    redis_password = ""

    # Tweet Configuration
    redis_key = 'tweets'
    num_tweets = 20

    def __init__(self):
        self.db = r = redis.Redis(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password
        )
        self.trim_count = 0

    def push(self, data):
        self.db.lpush(self.redis_key, json.dumps(data))
        self.trim_count += 1

        # Periodically trim the list so it doesn't grow too large.
        if self.trim_count > 100:
            self.db.ltrim(self.redis_key, 0, self.num_tweets)
            self.trim_count = 0

    def tweets(self, limit=15):
        tweets = []

        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item)
            tweets.append(tweet_obj)

        return tweets

    def reset_tweets(self):
        self.db.ltrim(self.redis_key, 0, 1)
        #self.db.delete( self.redis_key)


        return "Tweets key reset"

    
    def fetch_all(self, limit=15):
        print("Hello fetch all")
        tweets = []
        limit = self.db.llen(self.redis_key)
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item.decode('utf-8'))
            tweets.append(tweet_obj)
        print("My tweets : ", tweets)
        return tweets

    def fetch_user_report(self, keyword):
        tweets = []
        #d = defauldict(list)
        limit = self.db.llen(self.redis_key)
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item.decode('utf-8'))
            #simple_obj = defaultdict(list)
            if(keyword == tweet_obj['keyword']):
                user_name = tweet_obj['username']
                tweets.append(user_name )
        print("My tweets : ", Counter(tweets))
        return tweets
    
    def link_report(self):
        tweets = []
        #d = defauldict(list)
        limit = self.db.llen(self.redis_key)
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item.decode('utf-8'))
            #simple_obj = defaultdict(list)
            links = tweet_obj['urls']
            tweets.extend(links)
        #print("My tweets links : ", Counter(tweets))
        return tweets

        # for status in tweepy.Cursor(status.user_timeline, id=user, include_entities=True).items(20): 
        #     print(status.entities['urls'])
        #     exit()
            # for url in status.entities['urls']:
            #     print url['expanded_url']
    
    def content_report(self):
        stop_words = {'ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than'}
        tweets = []
        limit = self.db.llen(self.redis_key)
        for item in self.db.lrange(self.redis_key, 0, limit-1):
            tweet_obj = json.loads(item.decode('utf-8'))
            texts = tweet_obj['text']
            tweets.extend(texts.split())
        list_tweet_without_stop_words = list(filter(lambda w : not w in stop_words, tweets))

        return list_tweet_without_stop_words