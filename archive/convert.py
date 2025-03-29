import json
import os
import re
import shutil

shutil.rmtree("./data/cooked/")
os.mkdir("./data/cooked/")

print("> Converting raw tweet data to JSON")

with open("./data/raw/tweets.js", "r") as tweets_in,\
     open("./data/cooked/tweets.json", "w") as tweets_out:

    tweets = []
    new_tweet = {}
    counter = 0
    for line in tweets_in:
        
        time_match = re.search('"created_at" : "(.*?)",', line)
        if time_match != None:
            # timestamp = time.strptime(timestr.group(1), "%a %b %d %H:%M:%S %z %Y")
            new_tweet["timestamp"] = time_match.group(1)

            if counter != 0:
                print("ERROR: Two timestamps in a row")
                exit(0)
            counter = 1

        text_match = re.search(r'"full_text" : "(.*?)\\n(.*?)\\n(.*?)",', line)
        if text_match != None:
            post_dict = {}
            post_dict["course"] = text_match.group(1)
            post_dict["title"] = text_match.group(2)
            post_dict["price"] = text_match.group(3)
            new_tweet["post"] = post_dict

            if counter != 1:
                print("ERROR: Two texts in a row")
                exit(0)
            counter = 0

        skip_match = re.search(r'"Attention students!', line)
        if skip_match != None:
            counter = 0

        if "timestamp" in new_tweet and "post" in new_tweet:
            tweets.append(new_tweet)
            new_tweet = {}

    # Write
    json.dump(tweets, tweets_out, ensure_ascii=False, indent=4)

print("> Finished converting")