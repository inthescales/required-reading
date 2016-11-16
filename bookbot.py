import bookgen
import tweepy
from random import randint
import time
import locale

locale.setlocale(locale.LC_ALL, '')

def generate_tweet():

    valid = False
    while not valid:
        generated = bookgen.generate_for_tweet()
        course = generated[0].title() + " " + str(randint(100, 999))
        book = generated[1].title()
        cost = "$" + locale.format("%d", randint(99, 999), grouping=True)
        text = course + "\n" + book + "\n" + cost
        
        if len(text) <= 140:
            valid = True

    return text
    
class TwitterAPI:
    def __init__(self):
        consumer_key = "W8mx3eg7mA4J8pZjSE3gkPplN"
        consumer_secret = "iHh2ZWXcTrRtbToTV8q1QdkdsEZ9KIjsN7RgonfzOsyheyZkjt"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = "798422658425778176-at7rlU1vIugbbZ3hvvVIVLXvV93tNKB"
        access_token_secret = "N7ZlfS2yVI3JFNsO0osPz6VewV4KVXS6O0mhy9nCvFHKi"
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)

    def tweet(self, message):
        self.api.update_status(status=message)


twitter = TwitterAPI()

print "Starting up!"

while True:
    
    tweet = generate_tweet()
    
    if tweet:
        twitter.tweet(tweet)
        
    time.sleep(60 * 60)