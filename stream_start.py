import datetime
import json
import tweepy
from storeTweets import TweetStore
import time
import re
from collections import Counter 
from threading import Thread

path = '/home/basant/Documents/tweet_analysis/config.json'

with open(path) as f:
    tweet_config = json.loads(f.read())

consumer_key = tweet_config['consumer_key']
consumer_secret_key = tweet_config['consumer_secret_key']
access_token = tweet_config['access_token']
access_token_secret = tweet_config['access_token_secret']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
store = TweetStore()
staus_path = '/home/basant/Documents/tweet_analysis/status_print.json'

class TwitterListner(tweepy.StreamListener):
    def __init__(self,mins, keyword):
        super(TwitterListner, self).__init__()
        self.curr_time = time.time()
        self.end_time = time.time() + 60 * mins
        self.keyword = keyword
        
    def find(self,string): 
        # findall() has been used  
        # with valid conditions for urls in string 
        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
        return url 
      

    def on_status(self, status):
        """
        Override the on_status method of tweepy.StreamListener. 
        """
        json_str = json.dumps(status._json)
        
        # with open(staus_path, "w") as f:
        #     f.write( json_str )
        #exit()
        
        if('RT @' not in status.text):
            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', status.text)
            
            number_of_tweets = 200

            #get tweets
            tweets = api.user_timeline(screen_name = status.user.screen_name,count = number_of_tweets)

            for tweet in tweets:
                urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', tweet.text)
                all_urls = []
                for url in urls:
                    all_urls.append(url)
            
            tweet_item = {
                'text': status.text,
                'username': status.user.screen_name,
                'name': status.user.name,
                'profile_image_url': status.user.profile_image_url,
                #'keyword' : status.entities.get('hashtags')[0]['text'],
                'keyword' : self.keyword,
                #'urls' : status.entities.get('urls').expanded_url,
                'urls' : all_urls
            }


            
            while(self.curr_time <= self.end_time):
                store.push(tweet_item)
                print(tweet_item)
                staus_path = '/home/basant/Documents/tweet_analysis/user_report.txt'
                self.generate_reports()
                # if(time.time() >= self.curr_time + 50 and time.time() <= self.curr_time + 60):
                #     with open(staus_path, "a") as f:
                #         #f.write(" [1] : " + str(tweet_item) + '\n')
                #         #print(Counter(store.fetch_user_report("Mohansainikpuri")))
                #         Counter(store.fetch_user_report(self.keyword))
                #         f.write(" [1] : " + str(store.fetch_user_report(self.keyword)) + '\n')
                #         f.write(" [1] : " + str(Counter(store.fetch_user_report(self.keyword))) + '\n')
                #     print(tweet_item)
                    
                # if(time.time() >= self.curr_time + 60 and time.time() <= self.curr_time + 120):
                #     with open(staus_path, "w") as f:
                #         #f.write(" [2] : " +str(tweet_item) + '\n')
                #         f.write(" [1] : " + str(store.fetch_user_report(self.keyword)) + '\n')
                #         f.write(" [1] : " + str(Counter(store.fetch_user_report(self.keyword))) + '\n')
                #     print(tweet_item)

                # if(time.time() >= self.curr_time + 120 and  time.time() == self.curr_time + 180):
                #     with open(staus_path, "w") as f:
                        
                #         f.write(" [3] : " +str(tweet_item) + '\n')
                #     print(tweet_item)

                # if(time.time() >= self.curr_time + 180 and  time.time() == self.curr_time + 240):
                #     with open(staus_path, "w") as f:
                        
                #         f.write(" [4] : " +str(tweet_item) + '\n')
                #     print(tweet_item)

                # if(time.time() >= self.curr_time + 240 and  time.time() <= self.curr_time + 300):
                #     with open(staus_path, "w") as f:
                        
                #         f.write(" [5] : " +str(tweet_item) + '\n')
                #     print(tweet_item)
                
                if(time.time() >= self.curr_time + 300 ):
                    exit()

    def make_file_reports(self, minutes):
        user_path = '/home/basant/Documents/tweet_analysis/user_report.txt'
        content_path = '/home/basant/Documents/tweet_analysis/context_report.txt'
        link_path = '/home/basant/Documents/tweet_analysis/link_report.txt'
        with open(user_path, "a") as f:
            print("Generating repor of last ", minutes, " mins")
            user_data = store.fetch_user_report(self.keyword)
            print(user_data)
            f.write(" [" +str(minutes) + "] : " + str(user_data) + '\n')
            #f.write(" [" + str(minutes) + "] : "+ str(Counter(user_data)) + '\n')
        with open(content_path, "a") as f:
            content_data = store.content_report()
            print(content_data)
            f.write(" [" + str(minutes) + "] : "+  str(content_data) + '\n')
            #f.write(" [" + str(minutes) + "] : "+  str(Counter(content_data)) + '\n')
        with open(link_path, "a") as f:
            link_data = store.link_report()
            print(link_data)
            f.write(" [" + str(minutes) + "] : "+  str(link_data) + '\n')
            #f.write(" [" + str(minutes) + "] : "+  str(Counter(link_data)) + '\n')

    def generate_reports(self):
        while(True):
            if(time.time() >= self.curr_time + 55 and time.time() <= self.curr_time + 60):
                print("-------------------------")
                self.make_file_reports(1)
            if(time.time() >= self.curr_time + 110 and time.time() <= self.curr_time + 120):
                self.make_file_reports(2)
            if(time.time() >= self.curr_time + 178 and time.time() <= self.curr_time + 180):
                self.make_file_reports(3)
            if(time.time() >= self.curr_time + 238 and time.time() <= self.curr_time + 240):
                self.make_file_reports(4)
            if(time.time() >= self.curr_time + 298 and time.time() <= self.curr_time + 300):
                self.make_file_reports(5)
            if(time.time() >= self.curr_time + 300 ):
                    exit()

    def on_error(self, status_code):
        if status_code == 420:
            return False

print("Enter the list of keyword to search else enter stop. ")    
track_list = []
while(True):
    key = input()
    if(key == 'stop'):
        break
    track_list.append(key)

print(track_list)
print(store.reset_tweets())

#while(True):
print("Start here")
total_time = 2
tweet_listner = TwitterListner(total_time,track_list[0])
stream = tweepy.Stream(auth=api.auth, listener=tweet_listner)
# stream.filter(track=["#SaturdayMotivation","@narendramodi"])
t = Thread(target=tweet_listner.generate_reports)
t_stream = Thread(target=stream.filter(track=track_list))
t.start()
t_stream.start()

#print(store.fetch_all())

