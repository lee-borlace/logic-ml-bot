import json
import random

NUM_SAMPLES = 50

TRAIN_PERCENT = 0.8
VAL_PERCENT = 1 - TRAIN_PERCENT
TRAIN_COUNT = int(NUM_SAMPLES * TRAIN_PERCENT)
VAL_COUNT = int(NUM_SAMPLES * VAL_PERCENT)

SRC_TRAIN = "src-train.txt"
TGT_TRAIN = "tgt-train.txt"
SRC_VAL = "src-val.txt"
TGT_VAL = "tgt-val.txt"
SRC_VOCAB = "src-vocab.txt"
TGT_VOCAB = "tgt-vocab.txt"

random.seed()

# load vocab from JSON
print("Loading vocab...")
with open('vocab.json') as json_file:
    vocab = json.load(json_file)
print("Done.")

# Load templates
with open('training_templates.json') as json_file:
    training_templates = json.load(json_file)
    
# Data generation function
def generate_data(file_name_src, file_name_tgt, count):
    print(f"Generating {count} to {file_name_src} and {file_name_tgt}")
    
    out_file_src = open(file_name_src, "w+")
    out_file_tgt = open(file_name_tgt, "w+")

    for i in range(count-1) :
    
        # Grab a random example index
        index = random.randrange(0, len(training_templates))
        template = training_templates[index]
        
        # TODO : Do this more robustly.
        language = template['language'].strip()
        language = language.replace(',', '')
        language = language.replace('.', '')
        language = language.replace('(', '')
        language = language.replace(')', '')
        language = language.replace('-', '')
        
        generated_language_string = ""
        
        word_dict = {}
        
        for word in language.split(' '):
            word = word.strip()
            
            word_to_output = word
            
            if(word):
                #check if word contains POS
                pos_split = word.split('_')
                
                # Is a POS token - generate random permutation 
                if(pos_split and len(pos_split) == 3):
                    pos = pos_split[0]
                    index = pos_split[1]
                    tag = pos_split[2]
                    
                    word_dict_key = f"{pos}_{index}"
                    
                    if(pos in vocab) :
                        if(tag in vocab[pos]) :
                            if(len(vocab[pos][tag]) > 0) :
                                rand_index = random.randrange(0, len(vocab[pos][tag]))
                                rand_word = vocab[pos][tag][rand_index]['t']
                                word_to_output = str(rand_word)
                                
                                # Store lemma
                                word_dict[word_dict_key] = vocab[pos][tag][rand_index]['l']
                    
                generated_language_string += word_to_output + " "
            
        print(word_dict)
            
        logic = template['logic'].strip()
        
        generated_logic_string = ""
        
        for token in logic.split(' '): # TODO : split on something other than space!
            token = token.strip()
            
            token_to_output = token
            
            pos_split = token.split('_')
            
            if(pos_split and len(pos_split) == 2):
                if(token in word_dict) :
                    token_to_output = word_dict[token]
            
            generated_logic_string += token_to_output + " "
        
        out_file_src.write(generated_language_string.strip() + '\n')
        out_file_tgt.write(generated_logic_string.strip() + '\n')
        
        
        
        
generate_data(SRC_TRAIN, TGT_TRAIN, TRAIN_COUNT)
generate_data(SRC_VAL, TGT_VAL, VAL_COUNT)

print("DONE!")
    
