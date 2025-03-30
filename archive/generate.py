import json
import os
import shutil

import datetime
import time

shutil.rmtree("./output/")
os.mkdir("./output/")

def htmlForPost(post):
    return post["timestamp"] + "<br>" + post["post"]["course"] + "<br>" + post["post"]["title"] + "<br>" + post["post"]["price"] + "<br><br>"

print("> Generating page")

content = ""

with open("./templates/header.html", "r") as header,\
     open("./templates/footer.html", "r") as footer,\
     open("./data/cooked/tweets.json", "r") as file_in:

    start_time = None
    posts_read = 0

    days_limit = None
    posts_limit = 100
    finished = False

    content = header.read()

    posts = json.loads(file_in.read())
    for post in posts:
        timestamp = datetime.datetime.strptime(post["timestamp"], "%a %b %d %H:%M:%S %z %Y")
        # timestamp = datetime.fromtimestamp(post["timestamp"])
        if start_time == None:
            start_time = timestamp
        else:
            difference = start_time - timestamp
            if days_limit != None and difference >= datetime.timedelta(days=days_limit):
                finished = True
                print("> Finishing after " + str(days_limit) + " days of posts")

        if not finished:
            content += htmlForPost(post)
            posts_read += 1

            if posts_limit != None and posts_read >= posts_limit:
                finished = True
                print("> Finishing after " + str(posts_limit) + " posts")
        else:
            break

    content += footer.read()

    print("> Writing content")

    f = open("./output/index.html", "w")
    f.write(content)
    f.close()

print("> Finished")