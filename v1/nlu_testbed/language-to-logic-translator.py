# -*- coding: utf-8 -*-
from typing import Any, Dict, List
import spacy
from spacy.tokens import Token

# ****************************************************************************************************
# Result of a language to logic translation
# ****************************************************************************************************
class LanguageToLogicTranslationResult:
    
    # Confidence of match
    confidence = 0.0
    
    # Translation
    translation = ""

    def __init__(self, translation, confidence) -> None:
        self.confidence = confidence
        self.translation = translation
        
    def __str__(self) -> str:
        return f"{{confidence={self.confidence},translation={self.translation}}}"


# ****************************************************************************************************
# Spacy token augmented with information about whether it should be considered as the token itself
# or just its text        
# ****************************************************************************************************
class TokenWithTokenOrTextInfo:
    
    def __init__(self, token:Token, treatAsText:bool) -> None:
        self.token = token
        self.treatAsText = treatAsText
        
    def __str__(self) -> str:
        return f"{{treatAsText={self.treatAsText},token.text={self.token.text}}}"


# ****************************************************************************************************
# Result of a language to logic translation
# ****************************************************************************************************
class LanguageToLogicTranslator:
    
    # replacementStopWords : words which should not be turned into NLP tokens when attempting translation
    # via POS. E.g. if "the" is listed, then "the" will always just be treated as the string "the", when 
    # calculating replacement purmutations, rather than the corresponding prep POS.    
    def __init__(self, replacementStopWords:List[str]) -> None:
        self.replacementStopWords = replacementStopWords
    
    # Given a list of tokens, return all permutations if each token both treated as text or a token
    def getTokenReplacementPermutations(self, tokens:List[Token]) -> List[List[TokenWithTokenOrTextInfo]]:
        permutations = []
        
        # TODO : Properly add all permutations, taking into account replacementStopWords
        permutations.append([TokenWithTokenOrTextInfo(token, False) for token in tokens])
        return permutations
        
    
    # Take an input string in natural language, convert to logic
    def translateLanguageToLogic(self, languageString:str) -> List[LanguageToLogicTranslationResult]:
        translationResults = []

        doc = nlp(languageString)
        
        # Build up list of replacement variations (i.e. all permutations of replacing or not
        # replacing each token with its text)
        tokens = [token for token in doc]
        tokenReplacementVariations = self.getTokenReplacementPermutations(tokens)

        translationResults.append(LanguageToLogicTranslationResult("LogicStuff()", 0.5))
        
        return translationResults

# ****************************************************************************************************
# Testbed mainline
# ****************************************************************************************************

#MODEL = "en_core_web_lg"
MODEL = "en_core_web_sm"
nlp = spacy.load(MODEL)

input = "the dog chased the cat"

extractor = LanguageToLogicTranslator(["the", "a", "an"])
translationResults = extractor.translateLanguageToLogic(input)

if len(translationResults) > 0:
    print("Results-")
    
    for translationResult in translationResults:
        print(str(translationResult))
    
else:
    print("No results")
    


