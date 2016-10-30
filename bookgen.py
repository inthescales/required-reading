import json
import random
import re
import sys

data = {}
field = None
failed = False

with open('titles.json') as data_file:
    data["title"] = json.load(data_file)

with open('fields.json') as data_file:
    data["fields"] = json.load(data_file)

with open('texts.json') as data_file:
    data["text"] = json.load(data_file)

if data is None:
    print "Error: missing data"
    sys.exit()
    
def generate_title():
    global field
    title = random.choice(get_value("title:formats"))
    field = random.choice(get_value("fields:fields"))
    return random.choice( expand(title) )
    
def expand(node):
    expansions = list()    
    replacethese = re.findall(r'<.+?>', node)
    if len(replacethese) > 0:
        for to_replace in replacethese:
            if "#" in to_replace:
                number = to_replace.split("#")[1]
            else:
                number = None
            possibles = get_value(to_replace[1:-1])

            if len(possibles) > 1:
                at_least = 1
            else:
                at_least = 1
            for replacement in random.sample(possibles, at_least):
            
                if number is None:
                    replaced = node.replace(to_replace, replacement, 1)
                else:
                    replaced = node.replace(to_replace, replacement)
                    
                return expand(replaced)
    else:
        expansions.append(node)
    return expansions

def get_value(node):
    global field
    node = node.split("#")[0]
    tokens = node.split(":")
    dict = None
    
    if tokens[0] == "title":
        dict = data["title"]
    elif tokens[0] == "fields":
        dict = data["fields"]
    elif tokens[0] == "text":
        dict = data["text"]
    elif tokens[0] == "field":
        dict = field
    else:
        return "ERROR"
        failed = True
        
    cur = dict
    for token in tokens[1:]:
        if cur[token] is None:
            return "ERROR"
            failed = True
        else:
            cur = cur[token]
        
    return cur
        
print generate_title()

