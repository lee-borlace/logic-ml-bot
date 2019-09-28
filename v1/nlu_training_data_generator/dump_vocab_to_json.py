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

print(f"Total vocab count = {len(nlp.vocab)}") #1340242
MAX_WORDS_TO_PROCESS = 60000
print(f"Number of words to process = {MAX_WORDS_TO_PROCESS}")



pos_mapping = {}

sorted_vocab = sorted(nlp.vocab.__iter__(), key=lambda x: x.prob, reverse=True)

word_count = 0
for l in sorted_vocab :
    if(word_count == MAX_WORDS_TO_PROCESS) :
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