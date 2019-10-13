# -*- coding: utf-8 -*-
import re

class LogicService:
    def __init__(self, baseUrl):
        self.baseUrl = baseUrl
        
    def tell(self, sentence):
        
        REGEX_PATTERN_PRED = "([A-Z][A-Za-z0-9_]*)\s*\("
        REGEX_PATTERN_CONSTANT = "[\(\,]\s*([A-Z][A-Za-z0-9_]*)\s*[\)\,]"
        REGEX_PATTERN_VARIABLE = "[\(\,]\s*([a-z][A-Za-z0-9_]*)\s*[\)\,]"
        
        preds = []
        constants = []
        variables = []
        
        regex = re.compile(REGEX_PATTERN_PRED)
        matches = regex.findall(sentence)
        if matches :
            for match in matches:
                match = match.strip()
                if match not in preds:
                    preds.append(match)

        regex = re.compile(REGEX_PATTERN_CONSTANT)
        matches = regex.findall(sentence)
        if matches :
            for match in matches:
                match = match.strip()
                if match not in constants:
                    constants.append(match)

        regex = re.compile(REGEX_PATTERN_VARIABLE)
        matches = regex.findall(sentence)
        if matches :
            for match in matches:
                match = match.strip()
                if match not in variables:
                    variables.append(match)
        
        print("preds=" + str(preds))
        print("constants=" + str(constants))
        print("variables=" + str(variables))
                            
        
    def findAllWithOverlap(self, regex, seq):
        resultlist=[]
        pos=0
        while True:
            result = regex.search(seq, pos)
            if result is None:
                break
            # resultlist.append(seq[result.start():result.end()])
            resultlist.append(result.group(0))
            pos = result.start()+1
        return resultlist
            
    