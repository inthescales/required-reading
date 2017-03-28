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

keywords = list(set(keywords))

def prepare_data(data):
    mod = re.sub('[ \n\r]+', ' ', data)
    return mod
        
def find(keywords, file):

    file_data = None
    finds = {}
    
    with open(file, 'r') as corpus:
        file_data = corpus.read()
        file_data = file_data.decode("utf-8")
        file_data = prepare_data(file_data)
        
    words = file_data.split(" ")

    for i in range(0, len(words)):
        
        word = words[i].lower()
        
        if word and word in keywords:
            
            if word not in finds:
                finds[word] = []
            
            for j in range(0,5):
                if i-j > 0 and i-j+5 < len(words):
                    term = words[i-j:i-j+5]
                    cleaned = clean(word, term)
                    if cleaned:
                        #print cleaned
                        finds[word].append(" ".join(cleaned))
                        
    return finds

def clean(initial_word, term):
   
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
        return char == "," or char == "-"
        
    def breaking_punc(char):
        return char == "\"" or char == "(" or char == ")" or char == "." or char == ";" or char == ":" or char == "!" or char == "?" or char == "'"

    for i in reversed(range(0, len(term))):
            
        word = term[i]
        is_first = i == 0
        is_last = i == len(term)-1
        length = len(term)
        tags = []
        for i in 0..len(term):
            tags[i] = tag(word)
            
        
        # Clean initial punctuation
        first_char = word[0]
        if first_char == "\"" or first_char == "(" or first_char == "[" or first_char == "{":
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
        if not tags[i]:
            continue
            
        tags = tagged[0]
        if is_last and ('CC' in tags[i] or 'IN' in tags[i] or 'DT' in tags[i] or 'PRP' in tags[i] or 'PRP$' in tags[i] or 'WDT' in tags[i] or 'WP$' in tags[i] or 'MD' in tags[i] or 'TO' in tags[i] or 'WRB' in tags[i] or 'VB' in tags[i] or 'VBZ' in tags[i] or 'VBP' in tags[i] or 'VBD' in tags[i] or 'RB' in tags[i]):
            term = term[:i]
            continue
            
        if is_first and ('VB' in tags[i] or 'VBZ' in tags[i] or 'VBP' in tags[i] or 'VBD' in tags[i]):
            return None
    
    #print term
    
    if 'JJ' in tags[len(term)-1] and (term[len(term)-2] == "a" or term[len(term)-2] == "an"):
        return None
    
    if len(term) >= 3 and initial_word in term:
        return term
    else:
        return None

corpora = ['homer-odyssey.txt', 'bible.txt', 'blake-poems.txt', 'carroll-alice.txt', 'darwin-origin.txt', 'malleus.txt', 'marx-critique.txt', 'milton-paradise.txt', 'plato-republic.txt', 'shakespeare-hamlet.txt', 'declaration-of-independence.txt', 'oxford-american-essays.txt']

finds = {}
for corpus in corpora:
    print corpus
    terms = find(keywords, 'corpus/' + corpus)
    finds[corpus] = terms
    file = open('excerpts/' + corpus, 'w')
    dump = json.dumps(finds[corpus])
    file.write(dump)
    file.close()
