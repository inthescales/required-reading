import json
import random
import re
import sys
from os import listdir
from os.path import isfile, join
import locale
import string

locale.setlocale(locale.LC_ALL, '')

# Data Structures ============

class Entry:

    def __init__(self):
        self.field = None
        self.field_name = None
        self.modifier = None
        self.title = None

        self.courseNumber = 0
        self.price = 0

    def compose(self):
        field_name = random.choice(self.field["name"])
        course = string.capwords(field_name) + " " + str(random.randint(100, 999))
        book = string.capwords(self.title)
        cost = "$" + locale.format("%d", random.randint(99, 999), grouping=True)
        text = course + "\n" + book + "\n" + cost

        return text

# Globals and Reading Data ==========

class Generator:

    def __init__(self):
        self.data = {}
        self.excerpts = {}

    def read_data(self):

        contents_path = './contents/'

        with open(contents_path + 'titles.json') as data_file:
            self.data["title"] = json.load(data_file)

        with open(contents_path + 'fields.json') as data_file:
            self.data["fields"] = json.load(data_file)

        with open(contents_path + 'texts.json') as data_file:
            self.data["text"] = json.load(data_file)

            path = '.'
            excerpts_path = './excerpts/'
            excerpt_files = [f for f in listdir(excerpts_path) if isfile(join(excerpts_path, f))]

        for file in excerpt_files:
            if file[0] != '.':
                with open(excerpts_path + file) as data_file:
                    self.excerpts[file] = json.load(data_file)
    
                    if self.data is None:
                        print("Error: missing data")
                        sys.exit()

    def get_titles(self, field, modifier):

        titles = self.get_value("title:formats", field, modifier)
    
        return titles
    
        if "title" in field:
            titles.extend(self.get_value("field:title", field, modifier))
        
        if modifier:
            titles.extend(self.get_value("fields:modifier_titles", field, modifier))
            if "title" in modifier:
                titles.extend(self.get_value("modifier:title", field, modifier))
        else:
            titles.extend(self.get_value("title:no_modifier", field, modifier))

        return titles
    
    def get_keywords(self, field, modifier):
    
        keywords = []
    
        if "keyword" in field:
            keywords = field["keyword"]
    
        if modifier and "keyword" in modifier:
            keywords.extend(self.get_value("modifier:keyword"), field, modifier)

        return keywords
    
    def get_sources(self, field, modifier):
    
        sources = self.data["fields"]["source"]

        if "source" in field:
            sources.extend(field["source"])
    
        if modifier and "source" in modifier:
            sources = self.get_value("modifier:source", field, modifier)
    
        return sources

    def get_entry(self):

        entry = Entry()

        if random.random() <= 0.05:
            entry.modifier = self.get_modifier()

        entry.field = self.get_field(entry.modifier)
        entry.title = self.generate_title(entry.field, entry.modifier)

        return entry

    def generate_title(self, field, modifier):

        title_choices = self.get_titles(field, modifier)
        title = random.choice(title_choices)
    
        expand_data = {"taken": {}}
        titles = self.expand(title, expand_data, field, modifier)

        if "blacklist" in field:
            blacklist = field["blacklist"]
            titles = self.filter(titles, blacklist)
    
        if titles:
            return random.choice(titles)
        else:
            return None

    def get_modifier(self):
        modifier = random.choice(self.get_value("fields:modifiers", None, None))
        return modifier

    def get_field(self, modifier):

        field = dict(random.choice(self.get_value("fields:fields", None, modifier)))

        if modifier:
            field["name"] = [random.choice(modifier["adjective"]) + " " + random.choice(field["name"])]
        else:
            field["name"] = [random.choice(field["name"])]
        
        field["excerpts"] = self.get_excerpts(self.get_sources(field, modifier), self.get_keywords(field, modifier))
          
        return field        

    def filter(self, titles, blacklist):
        accepted = titles
        for title in titles:
            caught = False
            for word in blacklist:
                if word in title:
                    accepted.remove(title)
                    break
                
        return accepted
    
    def get_excerpts(self, sources, keywords):
    
        available = []
        for source in self.excerpts:
            if source in sources:
                for keyword in self.excerpts[source]:
                    if keyword in keywords:
                        available.extend(self.excerpts[source][keyword])
                    
        return available

    # Guts ========================

    def resolve_chance(self, node):
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
    
    def expand(self, node, data, field, modifier):
        expansions = list()
        node = self.resolve_chance(node)
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

                possibles = self.get_value(inner_text, field, modifier)
                if unique and to_replace in data["taken"]:
                    possibles = [item for item in possibles if item not in data["taken"][to_replace]]
                    if not possibles:
                        possibles = self.get_value(inner_text, field, modifier)
                
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
                
                return self.expand(replaced, data, field, modifier)
        else:
            expansions.append(node)

        return expansions

    def get_value(self, node, field, modifier):

        node = node.split("#")[0]
        tokens = node.split(":")
        dict = None
    
        if tokens[0] == "title":
            dict = self.data["title"]
        elif tokens[0] == "fields":
            dict = self.data["fields"]
        elif tokens[0] == "text":
            dict = self.data["text"]
        elif tokens[0] == "field":
            dict = field
        elif tokens[0] == "modifier":
            dict = modifier
        elif tokens[0] == "excerpt":
            excerpts = field["excerpts"]
            if excerpts:
                return excerpts
            else:
                print("Failed: invalid source or keyword")
                print(field["excerpts"])
                failed = True
                return ["ERROR"]
        
        cur = dict
        for token in tokens[1:]:

            if token not in cur:
                print("DIDN'T FIND " + token + " IN " + node)
                return None
            else:
                cur = cur[token]
        
        return cur

    # Action ==================

    def generate_entry(self):

        generated = None
        while generated == None or failed:
            failed = False
            generated = self.get_entry()
        
        return generated

def validate_tweet(text):

    if len(text) <= 140:
        return True
    else:
        return False

def write_tweet():

    generator = Generator()
    generator.read_data()
    valid = False

    while not valid:
        entry = generator.generate_entry()
        text = entry.compose()
        valid = validate_tweet(text)
        
        if len(text) <= 140:
            valid = True

    return text

def test(num):

    generator = Generator()
    generator.read_data()

    for i in range(0, num):
        entry = generator.generate_entry()
        text = entry.compose()
        print(text)
        print("")

