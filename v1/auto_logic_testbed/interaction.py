# -*- coding: utf-8 -*-
# This program prompts the user for text and anlayzes it. Each sentence is analyzed two ways - once as a complete unit, once on a word by word basis
import spacy
import json
from spacy import displacy
from logic_service import LogicService
import string
import random

random.seed()

MODEL = "en_core_web_lg"
nlp = spacy.load(MODEL)


LOGIC_SERVICE_BASE_URL = "http://localhost:8081"
CONSTANT_RANDOM_PREFIX_LENGTH = 4

# Load English tokenizer, tagger, parser, NER and word vectors


print("\exit or \quit to quit");

def print_token(token):
    print(f"TEXT={token.text},LEMMA={token.lemma_},POS={token.pos_},TAG={token.tag_},DEP={token.dep_},ID={token.i}")
    
def get_token_id_as_const(token, randomConstantPrefix) :
    return f"Const_{randomConstantPrefixThisSentence}_{token.i}"

def get_pos_formatted(token):
    return token.pos_.strip().lower().capitalize()

def get_lemma_formatted(token):
    
    lemma = token.lemma_.strip().lower().capitalize()
    
    if lemma == "-pron-":
        lemma = token.text.lower().capitalize()
    
    return lemma

def get_tag_formatted(token):
    return token.tag_.strip().lower().capitalize().replace("$","")

def get_dep_formatted(token):
    return token.dep_.strip().lower().capitalize()

def get_random_string(randomStringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(randomStringLength))


randomConstantPrefixThisSentence = get_random_string(CONSTANT_RANDOM_PREFIX_LENGTH)
logicService = LogicService(LOGIC_SERVICE_BASE_URL)


#text = "your dog chased my cat, and he was very scared"
#text = "your dog chased my cat"
text = "your dog chased me"

doc = nlp(text)

print("****************************************")
print("Result from complete sentence analysis")
print("****************************************")

for token in doc:
    print_token(token)

print()

print("****************************************")
print("Conversion to Logic")
print("****************************************")

sentences = []

for token in doc:
    
    pos_sentence = f"{get_pos_formatted(token)}({get_token_id_as_const(token, randomConstantPrefixThisSentence)},{get_lemma_formatted(token)},{get_tag_formatted(token)})"
    print(pos_sentence)
    sentences.append(pos_sentence)
    
    if token.i != token.head.i:
        dep_sentence = f"{get_dep_formatted(token)}({get_token_id_as_const(token, randomConstantPrefixThisSentence)},{get_token_id_as_const(token.head, randomConstantPrefixThisSentence)})"
        print(dep_sentence)
        sentences.append(dep_sentence)

logicService.tell(sentences)
        
        
        
        
        
