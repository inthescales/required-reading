import json
import re

from pattern.en import tag

field_data = None
keywords = []

with open ('fields.json', 'r') as keyfile:
    field_data = json.load(keyfile)
    
for field in field_data["fields"]:
    if "keyword" in field:
        keywords.extend(field["keyword"])
        
for modifier in field_data["modifiers"]:
    if "keyword" in modifier:
        keywords.extend(modifier["keyword"])

def prepare_data(data):
    mod = re.sub('[ \n\r]+', ' ', data)
    return mod
        
def find(keywords, file):

    file_data = None
    finds = {}
    
    with open(file, 'r') as corpus:
        file_data = corpus.read()
        file_data = prepare_data(file_data)
        
    words = file_data.split(" ")

    for i in range(0, len(words)):
        
        word = words[i].lower()
        
        if word in keywords:
            
            if word not in finds:
                finds[word] = []
            
            for j in range(0,5):
                if i-j > 0 and i-j+5 < len(words):
                    term = words[i-j:i-j+5]
                    if is_ok(term):
                        finds[word].extend(term)
                        print "ACCEPTED: " + " ".join(term)
                    else:
                        print "REJECTED: " + " ".join(term)

def clean(term)

    for i in range(0, len(term)-1):
    
        term[i] = term[i].replace("\"", "")
        
        word = term[i]
        is_last = i == len(term)-1
        last_char = word[len(word)-1]
        
        if is_last:
            if last_char == "." or last_char == ":" or last_char == "," or last_char == ";":
                term[i] = word[0:len(word)-2]
        
        if last_char == "." or last_char == ":":
            if not is_last:
                return False
            else:
                term[i] = word[0:len(word)-2]

def is_ok(term):

    first = term[0]
    first_tags = tag(first)[0]
    print first_tags
    if ('CC' in first_tags and 'and' not in first_tags):
        return False
                
    last = term[len(term)-1]
    last_tags = tag(last)[0]
    print last_tags
    if 'CC' in last_tags or 'IN' in last_tags or 'DT' in last_tags or 'PRP$' in last_tags or 'WDT' in last_tags or 'WP$' in last_tags or 'MD' in last_tags or 'TO' in last_tags or 'WRB' in last_tags or 'VB' in last_tags or 'RB' in last_tags: #MD: modal
        return False

    return True

#finds = find(["stone", "earth"], 'corpus/bible.txt')
finds = find(["stone", "earth"], 'corpus/marx_critique.txt')
print finds
