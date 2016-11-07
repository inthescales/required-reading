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
                    cleaned = clean(term)
                    if cleaned:
                        #print cleaned
                        finds[word].append(" ".join(cleaned))
                        
    return finds

def clean(term):
   
    #print term
    
    is_last = True
    is_first = False
    
    def trim_first(word):
        return word[1:]
    
    def trim_last(word):
        return word[:-1]
        
    def no_marks(word):
        return re.match('\w+', word)
        
    def non_breaking_punc(char):
        return char == ","
        
    def breaking_punc(char):
        return char == "\"" or char == "." or char == ";" or char == ":"

    for i in reversed(range(0, len(term))):
            
        word = term[i]
        is_first = i == 0
        is_last = i == len(term)-1
        length = len(term)
        
        # Clean initial punctuation
        first_char = word[0]
        if first_char == "\"":
            if not is_first:
                term = term[:i]
            else:
                term[i] = word[1:]
            continue
        
        # Clean final punctuation, break if necesssary
        for j in reversed(range(0, len(word))):
            cur = word[j]
            if non_breaking_punc(cur):
                term[i] = word = word[:-1]
            elif breaking_punc(cur):
                term[i] = word = word[:-1]
                term = term[:i+1]
                is_last = i == len(term)-1
                
        # Check category
        tags = tag(word)[0]
        if is_last and ('CC' in tags or 'IN' in tags or 'DT' in tags or 'PRP$' in tags or 'WDT' in tags or 'WP$' in tags or 'MD' in tags or 'TO' in tags or 'WRB' in tags or 'VB' in tags or 'VBZ' in tags or 'VBP' in tags or 'VBD' in tags or 'RB' in tags):
            term = term[:i]
            continue
            
        if is_first and ('VB' in tags or 'VBZ' in tags or 'VBP' in tags or 'VBD' in tags):
            return None
    
    #print term
    
    if len(term) >= 3:
        return term
    else:
        return None

#finds = find(["stone", "earth"], 'corpus/bible.txt')
finds = find(["stone", "earth"], 'corpus/marx_critique.txt')
print finds
