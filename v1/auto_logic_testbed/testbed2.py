import re


def tell(sentence):
    
#        REGEX_PATTERN_PRED = "([A-Z][A-Za-z0-9_]*)\s*\("
#        REGEX_PATTERN_CONSTANT = "[\(\,]\s*([A-Z][A-Za-z0-9_]*)\s*[\)\,]"
#        REGEX_PATTERN_VARIABLE = "[\(\,]\s*([a-z][A-Za-z0-9_]*)\s*[\)\,]"
    
    REGEX_PATTERN_PRED = "([A-Z][A-Za-z0-9_]*)\s*\("
    REGEX_PATTERN_CONSTANT = "[\(\,]\s*([A-Z][A-Za-z0-9_]*)\s*[\)\,]"
    REGEX_PATTERN_VARIABLE = "[\(\,]\s*([a-z][A-Za-z0-9_]*)\s*[\)\,]"
    
    preds = []
    constants = []
    variables = []
    
    regex = re.compile(REGEX_PATTERN_PRED)
    matches = findAllWithOverlap(regex, sentence)
    if matches :
        for match in matches:
            match = match.strip()
            if match not in preds:
                preds.append(match)

    regex = re.compile(REGEX_PATTERN_CONSTANT)
    matches = findAllWithOverlap(regex, sentence)
    if matches :
        for match in matches:
            match = match.strip()
            if match not in constants:
                constants.append(match)

    regex = re.compile(REGEX_PATTERN_VARIABLE)
    matches = findAllWithOverlap(regex, sentence)
    if matches :
        for match in matches:
            match = match.strip()
            if match not in variables:
                variables.append(match)
    
    print("preds=" + str(preds))
    print("constants=" + str(constants))
    print("variables=" + str(variables))
                        
    
def findAllWithOverlap(regex, seq):
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
        
#tell("Instance(Const1,Cilantro) AND Instance   (Const2,server)  AND  Verb(Const3,Say ,  Const1)  AND  VerbLink(Const3,  amidst2, Const2 )")
tell("Noun(Const_tdlg_1,a,Doggy,b,c,Broggy,Foggy,Blah,hrah,Nn)")