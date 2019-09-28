import spacy
import json
MODEL = "en_core_web_lg"
nlp = spacy.load(MODEL)

MAX_WORDS = 5000000000000

# A dict where the key is part of speech, and the value is a list of objects, each being a word from the vocab
# for that POS, and containing various elements of the word.
pos_mapping = {}

# Iterate over all lexemes in vocab
word_count = 0
for l in nlp.vocab.__iter__() :
    
    if(word_count == MAX_WORDS) :
        break
    
    word_count += 1
    
    if(l.is_alpha and (not l.is_oov) and (not l.is_stop) and (not l.is_punct)) :
        doc = nlp(l.text) # Analyse. This won't be 100% accurate as we're just analysing one word but should be good enough!
        for token in doc :
            
            if(token.pos_ == "NOUN"):
                print(f"t:{token.text},l:{token.lemma_},p:{token.pos_},tg:{token.tag_}")
            
