import bookgen
from random import randint
import locale

locale.setlocale(locale.LC_ALL, '')

def generate_tweet():

    valid = False
    while not valid:
        generated = bookgen.generate_for_tweet()
        course = generated[0] + " " + str(randint(100, 999))
        book = generated[1]
        cost = "$" + locale.format("%d", randint(99, 9999), grouping=True)
        text = course + "\n" + book + "\n" + cost
        
        if len(text) <= 140:
            valid = True

    print text
    
generate_tweet()