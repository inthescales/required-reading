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
    field = get_field()
    
    data = {"taken": {}}
    
    return random.choice( expand(title, data) )
    
def get_field():
    field = random.choice(get_value("fields:fields"))
    if random.random() <= 0.6:
        modifier = random.choice(get_value("fields:modifiers"))
        field["name"] = [random.choice(modifier["adjective"]) + " " + random.choice(field["name"])]
        if "object" in field and "object" in modifier:
            field["object"].extend(modifier["object"])
    else:
        field["name"] = [random.choice(field["name"])] # choose one name for the field
        
    return field
    
def resolve_chance(node):
    chances = re.findall(r'\[.+?(?:\|\d\d)?(?:#\d+)?\]', node)
    
    handled_groups = [] #skip groups that have already been resolved
    
    if len(chances) > 0:
        for chance in chances:
            inner = chance[1:-1]
            if "#" in chance:
                split = inner.split("#")
                inner = split[0]
                group = split[1]
                if group in handled_groups:
                    continue
            else:
                group = None
                
            if "|" in chance:
                split = inner.split("|")
                inner = split[0]
                probability_string = split[1]
                probability = float(split[1]) / 100
            else:
                probability_string = None
                probability = None
            
            if probability and random.random() < probability:
                replacement = inner
            else:
                replacement = ""
            
            if group is None:
                node = node.replace(chance, replacement, 1)
            else:
                node = re.sub(r'\[.+?(?:\|\d\d)?(?:#' + group + ')?\]', replacement, node)
                handled_groups.append(group)

    return node
    
def expand(node, data):
    expansions = list()
    node = resolve_chance(node)
    replacethese = re.findall(r'<.+?>', node)
    
    if len(replacethese) > 0:
        for to_replace in replacethese:
        
            inner_text = to_replace[1:-1]
            
            if '!' in to_replace:
                inner_text = inner_text[0:-1]
                unique = True
            else:
                unique = False
                
            if "#" in to_replace:
                number = inner_text.split("#")[1]
            else:
                number = None

            possibles = get_value(inner_text)
            if unique and to_replace in data["taken"]:
                possibles = [item for item in possibles if item not in data["taken"][to_replace]]
                if not possibles:
                    possibles = get_value(inner_text)
                
            replacement = random.choice(possibles)
            
            if unique:
                if to_replace in data["taken"]:
                    data["taken"][to_replace].append(replacement)
                else:
                    data["taken"][to_replace] = [replacement]
            
            if number is None:
                replaced = node.replace(to_replace, replacement, 1)
            else:
                replaced = node.replace(to_replace, replacement)
                
            return expand(replaced, data)
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
        if token not in cur:
            return ""
            failed = True
        else:
            cur = cur[token]
        
    return cur
        
print generate_title()

if failed:
    print "ERROR"

