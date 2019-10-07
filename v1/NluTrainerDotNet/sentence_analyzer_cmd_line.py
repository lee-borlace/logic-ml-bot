import sys
import spacy

MODEL = "en_core_web_lg"
text = "hello how are you"

if(len(sys.argv) == 2):
    text = str(sys.argv[1])

nlp = spacy.load(MODEL)
doc = nlp(text)

output = []

for token in doc:
    output.append({'t':token.text,'l':token.lemma_,'p':token.pos_,'tg':token.tag_})

print(output)


