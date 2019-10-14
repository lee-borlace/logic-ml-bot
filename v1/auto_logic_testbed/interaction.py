# -*- coding: utf-8 -*-
# This program prompts the user for text and anlayzes it. Each sentence is analyzed two ways - once as a complete unit, once on a word by word basis
import spacy
import json
from logic_service import LogicService
import sys

LOGIC_SERVICE_BASE_URL = "http://localhost:8081"
# MODEL = "en_core_web_lg"
MODEL = "en_core_web_sm"

print("\exit or \quit to quit")

logicService = LogicService(MODEL, LOGIC_SERVICE_BASE_URL)

print("\exit or \quit to quit")

while True:
    try:
        text = input("Input > ")
        
        if(text == "\exit" or text == "\quit"):
            break
        
        logicService.processNaturalLanguageSentence(text)

    except:
        print("Unexpected error:", sys.exc_info()[0])
            
            
        
        
        
