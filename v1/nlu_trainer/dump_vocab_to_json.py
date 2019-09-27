# Spit out complete spacy vocab as JSON, keyed by part of speech
#
# to run :
# 
# python dump_vocab_to_json.py > vocab.json

# Load spacy model
import spacy
import json
import re
MODEL = "en_core_web_lg"
nlp = spacy.load(MODEL)

MAX_WORDS = 1000

pos_mapping = {}

# Iterate over all lexemes in vocab
word_count = 0
for l in nlp.vocab.__iter__() :
    
    if(word_count == MAX_WORDS) :
        break
    
    word_count += 1
    
    if(l.is_alpha and (not l.is_oov) and (not l.is_stop) and (not l.is_punct) and re.match(r"[a-zA-Z]+", l.text)) :
        doc = nlp(l.text) # Analyse. This won't be 100% accurate as we're just analysing one word but should be good enough!
        for token in doc :
            pos = token.pos_
            tag = token.tag_
            
            if not pos in pos_mapping :
                pos_mapping[pos] = {}
                
            if not tag in pos_mapping[pos]:
                pos_mapping[pos][tag] = []
                
            pos_mapping[pos][tag].append({'t':token.text,'l':token.lemma_,'p':token.pos_,'tg':token.tag_})
            
out_file = open("vocab.json", "w+")
out_file.write(json.dumps(pos_mapping))