import spacy

# Comment in a large or small model depending on how long you want to wait :)
#MODEL = "en_core_web_sm"
MODEL = "en_core_web_lg"

# Load English tokenizer, tagger, parser, NER and word vectors
nlp = spacy.load(MODEL)

print("\exit or \quit to quit");

while True:
    text = input("Input>")
    
    if(input == "\exit" or input == "\quit"):
        break
    
    doc = nlp(text)
    for token in doc:
        print(f"TEXT={token.text},LEMMA={token.lemma_},POS={token.pos_},TAG={token.tag_},DEP={token.dep_}")



