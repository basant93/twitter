from storeTweets import TweetStore
from collections import Counter 


store = TweetStore()

# print(store.fetch_all())
print(Counter(store.fetch_user_report("Mohansainikpuri")))

#print(store.link_report())

tweets_content = store.content_report()
print(tweets_content)
print(Counter(tweets_content))