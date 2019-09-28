import json
import random
import re

NUM_SAMPLES = 1000

TRAIN_PERCENT = 0.7
VAL_PERCENT = 0.15
TEST_PERCENT = 0.15

TRAIN_COUNT = int(NUM_SAMPLES * TRAIN_PERCENT)
VAL_COUNT = int(NUM_SAMPLES * VAL_PERCENT)
TEST_COUNT = int(NUM_SAMPLES * TEST_PERCENT)

SRC_TRAIN = "src-train.txt"
TGT_TRAIN = "tgt-train.txt"

SRC_VAL = "src-val.txt"
TGT_VAL = "tgt-val.txt"

SRC_TEST = "src-test.txt"
TGT_TEST = "tgt-test.txt"

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
    
    out_file_src = open(file_name_src, "w+", encoding="utf-8")
    out_file_tgt = open(file_name_tgt, "w+", encoding="utf-8")

    for i in range(count-1) :
    
        # Grab a random example index
        index = random.randrange(0, len(training_templates))
        template = training_templates[index]
        
        # TODO : Do this cleanup more robustly.
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
            
            # By default we'll just output the word, unless it turns out to be a POS later
            word_to_output = word
            
            if(word):
                #check if word contains POS (i.e. it has "_" in it e.g. NOUN_1_NN)
                pos_split = word.split('_')
                
                # Is a POS token if it contains 3 elements when splitting on "_" - generate random permutation 
                if(pos_split and len(pos_split) == 3):
                    
                    # Split up based on template NOUN_1_NN
                    pos = pos_split[0]
                    index = pos_split[1]
                    tag = pos_split[2]
                    
                    # We will store the lemma of the word in a dict where the key is for example just NOUN_1
                    word_dict_key = f"{pos}_{index}"
                    
                    # We have the POS in the vocab dict
                    if(pos in vocab) :
                        # We have the tag in the vocab dict against the POS
                        if(tag in vocab[pos]) :
                            # There is at least 1 word against the POS and tag
                            if(len(vocab[pos][tag]) > 0) :
                                # Pick a random word from the list for the POS + tag
                                rand_index = random.randrange(0, len(vocab[pos][tag]))
                                rand_word = vocab[pos][tag][rand_index]['t']
                                word_to_output = str(rand_word).lower()
                                
                                # Store lemma in dict
                                word_dict[word_dict_key] = vocab[pos][tag][rand_index]['l']
                    
                generated_language_string += word_to_output + " "
            
        logic = template['logic'].strip()
        
        # Tokens to output
        generated_logic_sequence = []
        
        # pattern for splitting logic sentence
        REGEX_PATTERN = "([a-zA-Z0-9]+_[a-zA-Z0-9]+)|(AND)|(\()|(\))|(\s+)|(=>)|([a-zA-Z0-9]+)|(,)"
        
        matches = re.findall(REGEX_PATTERN, logic)
        
        # Iterate through matches
        for match in matches:
            
            # If the first element of the is present then we have a POS, so try to match it back
            if(match[0]) :
                token = match[0].strip()

                if(token in word_dict) :
                    token_to_output = word_dict[token].capitalize()

            # Else not present - we don't have a POS, so just search for the first element of the match which
            # is present and output that
            else:
                for token in match:
                    if(token):
                        token_to_output = token
                        break
                
            generated_logic_sequence.append(token_to_output)
        
        out_file_src.write(generated_language_string.strip() + '\n')
        
        # Output the logic sequence
        prev_token = ""
        for logic_token in generated_logic_sequence :
            # Make sure each token is separated from the previous one with a space
            if prev_token:
                if( (not prev_token.endswith(" ")) and (not prev_token.endswith("\t"))):
                    out_file_tgt.write(" ")
            
            out_file_tgt.write(logic_token)
            
            prev_token = logic_token
            
        # Finish the logic line with a newline
        out_file_tgt.write('\n')
        
        
generate_data(SRC_TRAIN, TGT_TRAIN, TRAIN_COUNT)
generate_data(SRC_VAL, TGT_VAL, VAL_COUNT)
generate_data(SRC_TEST, TGT_TEST, VAL_COUNT)

print("DONE!")
    
