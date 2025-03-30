import json
import os
import shutil

import datetime
import locale

locale.setlocale(locale.LC_TIME, "en_US")

shutil.rmtree("./output/")
os.mkdir("./output/")

def get_time_string(datetime):
    return datetime.strftime("%b %d %Y, %I:%M%p")

def html_for_post(template, time_string, post):
    html = template
    html = html.replace("%TIMESTAMP%", time_string)
    html = html.replace("%COURSE%", post["course"])
    html = html.replace("%TITLE%", post["title"])
    html = html.replace("%PRICE%", post["price"])
    return html

print("> Generating page")

content = ""

with open("./templates/header.html", "r") as header,\
     open("./templates/footer.html", "r") as footer,\
     open("./templates/post.html", "r") as post_template_in,\
     open("./data/cooked/tweets.json", "r") as file_in:

    start_time = None
    posts_read = 0

    days_limit = None
    posts_limit = 100
    finished = False

    content = header.read()
    post_template = post_template_in.read()

    posts = json.loads(file_in.read())
    for post in posts:
        timestamp = datetime.datetime.strptime(post["timestamp"], "%a %b %d %H:%M:%S %z %Y")
        if start_time == None:
            start_time = timestamp
        else:
            difference = start_time - timestamp
            if days_limit != None and difference >= datetime.timedelta(days=days_limit):
                finished = True
                print("> Finishing after " + str(days_limit) + " days of posts")

        if not finished:
            content += html_for_post(post_template, get_time_string(timestamp), post["post"])
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