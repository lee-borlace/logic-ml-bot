# -*- coding: utf-8 -*-
import re
import requests
import json
import spacy
import random
import string

class LogicService:
    
    # **********************************************************
    # Create a new logic service. Specify the base URL of the AIMI logic service API
    # **********************************************************
    def __init__(self, spacyModel, baseUrl):
        self.nlp = spacy.load(spacyModel)
        random.seed()
        self.baseUrl = baseUrl.strip()


    # **********************************************************
    # Process natural language sentence
    # **********************************************************
    def processNaturalLanguageSentence(self, nlpSentence):

        doc = self.nlp(nlpSentence)
        CONSTANT_RANDOM_PREFIX_LENGTH = 4
        randomConstantPrefixThisSentence = self.__get_random_string(CONSTANT_RANDOM_PREFIX_LENGTH)

        print("****************************************")
        print("Result from complete sentence analysis")
        print("****************************************")

        for token in doc:
            self.__print_token(token)

        print()

        print("****************************************")
        print("Conversion to Logic")
        print("****************************************")

        sentences = []

        for token in doc:
            
            pos_sentence = f"Spc_Pos_{self.__get_pos_formatted(token)}({self.__get_token_id_as_const(token, randomConstantPrefixThisSentence)},{self.__get_lemma_formatted(token)},{self.__get_tag_formatted(token)})"
            print(pos_sentence)
            sentences.append(pos_sentence)
            
            if token.i != token.head.i:
                dep_sentence = f"Spc_Dep_{self.__get_dep_formatted(token)}({self.__get_token_id_as_const(token, randomConstantPrefixThisSentence)},{self.__get_token_id_as_const(token.head, randomConstantPrefixThisSentence)})"
                print(dep_sentence)
                sentences.append(dep_sentence)

        self.tell(sentences)


    # **********************************************************
    # Add a new sentence to the KB
    # **********************************************************
    def tell(self, sentences):

        allPreds = []
        allConstants = []
        allVariables = []
        allSentences = []
        
        for sentence in sentences:
            sentence = sentence.replace(" ", "")
            allSentences.append(sentence)
            
            preds, constants, variables = self.__getPredsConstantsVariables(sentence)
            
            for pred in preds:
                if pred not in allPreds:
                    allPreds.append(pred)
                
            for constant in constants:
                if constant not in allConstants:
                    allConstants.append(constant)
    
            for variable in variables:
                if variable not in allVariables:
                    allVariables.append(variable)
        
        self.__makeRemoteTellRequest(allSentences, allPreds, allConstants, allVariables)

    # **********************************************************
    # Make request to remote logic service
    # **********************************************************
    def __makeRemoteTellRequest(self, sentences, preds, constants, variables) :
        
        baseUrl = self.baseUrl
        if not self.baseUrl.endswith("/"):
            baseUrl =  self.baseUrl + "/"
            
        url = baseUrl + "api/tell"
        requestData = { "sentences" : sentences, "predicates" : preds, "constants" : constants, "functions" : []  } 
        headers = {"Content-type": "application/json"}           
        r = requests.post(url = url, json = requestData, headers = headers)
        
        
    # **********************************************************
    # Ask a question from the KB
    # **********************************************************
    def ask(self, sentence):
        
        sentence = sentence.replace(" ", "")
        preds, constants, variables = self.__getPredsConstantsVariables(sentence)
        result = self.__makeRemoteAskRequest(sentence, preds, constants, variables) 
        return result
        
    # **********************************************************
    # Make request to remote logic service
    # **********************************************************
    def __makeRemoteAskRequest(self, sentence, preds, constants, variables) :
        
        baseUrl = self.baseUrl
        if not self.baseUrl.endswith("/"):
            baseUrl =  self.baseUrl + "/"
            
        url = baseUrl + "api/ask"
        requestData = { "query" : sentence, "predicates" : preds, "constants" : constants, "functions" : []  } 
        headers = {"Content-type": "application/json"}           
        r = requests.post(url = url, json = requestData, headers = headers)                            
        return r.json()
                          
    # **********************************************************
    # Determine the predicates, constants and variables in a sentence
    # **********************************************************
    def __getPredsConstantsVariables(self, sentence):
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
        matches = self.__findAllWithOverlap(regex, sentence)
        if matches :
            for match in matches:
                match = match.strip()
                if match not in constants:
                    constants.append(match)

        regex = re.compile(REGEX_PATTERN_VARIABLE)
        matches = self.__findAllWithOverlap(regex, sentence)
        if matches :
            for match in matches:
                match = match.strip()
                if match not in variables:
                    variables.append(match)
        
        return preds, constants, variables
        
        
    # **********************************************************
    # Regex helper method
    # **********************************************************
    def __findAllWithOverlap(self, regex, seq):
        resultlist=[]
        pos=0
        while True:
            result = regex.search(seq, pos)
    
            if result is None:
                break
            # resultlist.append(seq[result.start():result.end()])
            resultlist.append(result.group(1))
            pos = result.start()+1
        return resultlist
            


    def __get_token_id_as_const(self, token, randomConstantPrefixThisSentence) :
        return f"Spc_Cnst_{randomConstantPrefixThisSentence}_{token.i}"
        #return f"Const_{token.i}"

    def __get_pos_formatted(self, token):
        return token.pos_.strip().lower().capitalize()

    def __get_lemma_formatted(self, token):
        
        lemma = token.lemma_.strip().lower().capitalize()
        
        if lemma == "-pron-":
            lemma = token.text.lower().capitalize()
        
        return lemma

    def __get_tag_formatted(self, token):
        return token.tag_.strip().lower().capitalize().replace("$","")

    def __get_dep_formatted(self, token):
        return token.dep_.strip().lower().capitalize()

    def __get_random_string(self, randomStringLength):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(randomStringLength))
    
    def __print_token(self, token):
        print(f"TEXT={token.text},LEMMA={token.lemma_},POS={token.pos_},TAG={token.tag_},DEP={token.dep_},ID={token.i}")