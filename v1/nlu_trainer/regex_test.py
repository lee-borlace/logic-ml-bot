# -*- coding: utf-8 -*-
import re
input = "Verb(Const1, VERB_1, Const2, Const3) AND VerbTense(Const1, Past) AND Instance(Const2, NOUN_1) => Instance(Const3, NOUN_2)"
matches = re.findall("([a-zA-Z0-9]+_[a-zA-Z0-9]+)|(AND)|(\()|(\))|(\s+)|(=>)|([a-zA-Z0-9]+)|(,)", input)


for match in matches:
    for token in match:
        if(token):
            print(token)
        
    
