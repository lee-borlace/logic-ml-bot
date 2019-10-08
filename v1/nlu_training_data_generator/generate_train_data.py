import json
import random
import re
import sys
import numpy as np

NUM_SAMPLES = 10000

TRAIN_PERCENT = 0.7
VAL_PERCENT = 0.15
TEST_PERCENT = 0.15

ENGLISH_TRAIN = "english-train.txt"
LOGIC_TRAIN = "logic-train.txt"

ENGLISH_VAL = "english-val.txt"
LOGIC_VAL = "logic-val.txt"

ENGLISH_TEST = "english-test.txt"
LOGIC_TEST = "logic-test.txt"

# These let us add some random errors into the natural language training data to hopefully make it more robust
RATE_WORD_ORDER_SWAP = 0.0001 # Randomly swap the order of any word with its predecessor
RATE_WRONG_POS_TAG = 0.0001 # Randomly use the wrong POS tag e.g. eat instead of ate
RATE_DROP_WORD = 0.00001 # Randomly drop a word from the training example

# For examples marked as questions, this is the rate at which to ensure a question mark is on the end. This would ideally be the rate at which people
# actually use question marks when asking a question. E.g. if you expect people to correctly use a question mark when asking a bot a question
# 75% of the time, then set to 0.75
RATE_APPEND_QUESTION_MARK = 0.75 

OUTPUT_PATH = "."

VOCAB_FILE_NAME = "vocab.100k.json"
TEMPLATES_FILE_NAME = "training_templates.json"

VOCAB_BASE_PATH = "C:\\Users\\LeeBorlace\\Documents\\GitHub\\logic-ml-bot\\v1\\nlu_training_data_generator\\"
TEMPLATES_BASE_PATH = "C:\\Users\\LeeBorlace\\Documents\\GitHub\\logic-ml-bot\\v1\\nlu_training_data_generator\\"

VOCAB_PATH = VOCAB_BASE_PATH + VOCAB_FILE_NAME
TEMPLATES_PATH = TEMPLATES_BASE_PATH + TEMPLATES_FILE_NAME

# Get a normally distributed random number most highly concentrated around min_val and least highly around max_val
def normal_distribution_random(min_val, max_val):
    # Get a random number between 0 and 1, distributed normally around 0
    mu, sigma = 0, 0.26
    sample = abs(np.random.normal(mu, sigma, 1)[0])
    number_range = max_val-min_val+1
    retval = int(min_val + (number_range * sample))
    return min(retval, max_val)


def show_usage():
    print("Generates training data in current directory.")
    print()
    print("Usage :")
    print()
    print("python.exe generate_train_data.py NUM_SAMPLES TRAIN_PERCENT VAL_PERCENT TEST_PERCENT RATE_WORD_ORDER_SWAP RATE_WRONG_POS_TAG RATE_DROP_WORD VOCAB_PATH TEMPLATES_PATH RATE_APPEND_QUESTION_MARK OUTPUT_PATH")
    exit()

# If we've passed any args at all, then make sure they're correct. If no args then we just fall back to default
if(len(sys.argv) > 1):
    if(len(sys.argv) == 12):
        try:
            NUM_SAMPLES = int(str(sys.argv[1]))
            TRAIN_PERCENT = float(str(sys.argv[2]))
            VAL_PERCENT = float(str(sys.argv[3]))
            TEST_PERCENT = float(str(sys.argv[4]))
            RATE_WORD_ORDER_SWAP = float(str(sys.argv[5]))
            RATE_WRONG_POS_TAG = float(str(sys.argv[6]))
            RATE_DROP_WORD = float(str(sys.argv[7]))
            VOCAB_PATH = str(sys.argv[8])
            TEMPLATES_PATH = str(sys.argv[9])
            RATE_APPEND_QUESTION_MARK = float(str(sys.argv[10]))
            OUTPUT_PATH = str(sys.argv[11])
        except:
            show_usage()
    else:
        show_usage()

TRAIN_COUNT = int(NUM_SAMPLES * TRAIN_PERCENT)
VAL_COUNT = int(NUM_SAMPLES * VAL_PERCENT)
TEST_COUNT = int(NUM_SAMPLES * TEST_PERCENT)
    
random.seed()

# load vocab from JSON
print("Loading vocab...")
with open(VOCAB_PATH) as json_file:
    vocab = json.load(json_file)
print("Done.")

# Load templates
with open(TEMPLATES_PATH) as json_file:
    training_templates = json.load(json_file)

# Put templates in a dictionary keyed by frequency. Note that this has keys with range 1-10 inclusive
template_freq_dict = {}
for i in range(10) :
    template_freq_dict[i+1] = []

for template in training_templates :
     template_freq_dict[template["Frequency"]].append(template) 


 # Select a random frequency. The chance of selecting that frequency increases
 # with the freq, i.e. 10 will be selected more often than 1. TODO : This needs a more elegant / configurable solution!!
def get_random_frequency() :
    rand_number = random.randint(0,101)
    selected_frequency = 1
    
    if rand_number <= 1.8:
        selected_frequency = 1
    elif rand_number <= 5.4 :
        selected_frequency = 2
    elif rand_number <= 10.8 :
        selected_frequency = 3        
    elif rand_number <= 18 :
        selected_frequency = 4
    elif rand_number <= 27 :
        selected_frequency = 5
    elif rand_number <= 37.8 :
        selected_frequency = 6
    elif rand_number <= 50.4 :
        selected_frequency = 7
    elif rand_number <= 64.8 :
        selected_frequency = 8    
    elif rand_number <= 81 :
        selected_frequency = 9  
    else :
        selected_frequency = 10    
        
    return selected_frequency

# Get a random template. The chance of getting any particular template
# depends on its frequency. 
def get_random_template() :

    freq = get_random_frequency()
    template_count_for_freq = len(template_freq_dict[freq])
    
    # If we get a freq with no templates against it, pick another one till we
    # get one with templates
    while template_count_for_freq == 0 :
        freq = get_random_frequency()
        template_count_for_freq = len(template_freq_dict[freq])
      
    # Grab a random template index for the chosen frequency
    random_template_index = random.randrange(0, template_count_for_freq)
    
    return template_freq_dict[freq][random_template_index]

    
# Data generation function
def generate_data(file_name_src, file_name_tgt, count):
    print(f"Generating {count} to {file_name_src} and {file_name_tgt}")
    
    out_file_src = open(OUTPUT_PATH + "\\" + file_name_src, "w+", encoding="utf-8")
    out_file_tgt = open(OUTPUT_PATH + "\\" + file_name_tgt, "w+", encoding="utf-8")

    language_vocab_this_file = {}
    logic_vocab_this_file = {}

    for i in range(count-1) :
    
        # Grab a random example index
        template = get_random_template()
        
        # *************************************************
        # Deal with language example
        # *************************************************
        
        # TODO : Do this cleanup of punctuation more robustly.
        language = template['Language'].strip()
        language = language.replace(',', '')
        language = language.replace('.', '')
        language = language.replace('(', '')
        language = language.replace(')', '')
        language = language.replace('-', '')
        
        logic = template['Logic'].strip()

        # Skip any examples which don't have language or logic component
        if not language or not logic :
            continue

        word_dict = {}
        
        generated_language_sequence = []
        
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
                        
                        # Check whether to randomly make an error for the POS tag
                        if random.uniform(0, 1) < RATE_WRONG_POS_TAG :
                            tag_length_for_pos = len(vocab[pos].keys())
                            random_tag_index = random.randrange(0, tag_length_for_pos)
                            tag = list(vocab[pos].keys())[random_tag_index]
                        
                        # We have the tag in the vocab dict against the POS
                        if(tag in vocab[pos]) :
                            # There is at least 1 word against the POS and tag
                            if(len(vocab[pos][tag]) > 0) :
                                # Pick a random word from the list for the POS + tag
                                
                                #rand_index = random.randrange(0, len(vocab[pos][tag]))
                                rand_index = normal_distribution_random(0, len(vocab[pos][tag])-1)
                                
                                rand_word = vocab[pos][tag][rand_index]['t']
                                word_to_output = str(rand_word).lower()
                                
                                # Store lemma in dict
                                word_dict[word_dict_key] = vocab[pos][tag][rand_index]['l']
                        # Tag isn't in vocab for POS
                        else:
                            continue
                                
                    # POS isn't in vocab
                    else:
                        continue
                    
                    
                generated_language_sequence.append(word_to_output)
        
        # Output language sequence
        prev_token = ""
        token_index = 0
        
        output_string = ""
        
        for language_token in generated_language_sequence :

            if not language_token in language_vocab_this_file:
                language_vocab_this_file[language_token] = True
            
            # Check for random word swap - if swapping, then swap with the next word if there is one
            swapped_word = False
            if random.uniform(0, 1) < RATE_WORD_ORDER_SWAP :
                if token_index < len(generated_language_sequence)-1 :
                    swapped_word = True
                    original_word_this_token = language_token
                    language_token = generated_language_sequence[token_index+1]
                    generated_language_sequence[token_index+1] = original_word_this_token
            
            # Check for random word drop - if dropping the word, do nothing with this token and move to the next. Don't
            # do this if we also swapped a word
            if random.uniform(0, 1) < RATE_DROP_WORD and not swapped_word :
                token_index += 1
                continue
            
            output_string += language_token
            
            if token_index < len(generated_language_sequence)-1 :
                output_string += " "
            token_index += 1
            
            prev_token = language_token
        
        output_string = output_string.strip()
        
        # Determine whether or not to put a question mark at the end of a question
        if template["SentenceType"] == "Question":
            
            # Should end in a question mark
            if random.uniform(0, 1) < RATE_APPEND_QUESTION_MARK :
                if not output_string.endswith("?"):
                    output_string = output_string + " ?"
            # Should not end in a question mark
            else:
                if output_string.endswith("?"):
                    output_string = output_string.rstrip("?")
            
        
        out_file_src.write(output_string + '\n')
        
        
        # *************************************************
        # Deal with logic example
        # *************************************************        

        # Tokens to output
        generated_logic_sequence = []
        
        # pattern for splitting logic sentence
        REGEX_PATTERN = "([a-zA-Z0-9]+_[a-zA-Z0-9]+)|(AND)|(\()|(\))|(\s+)|(=>)|([a-zA-Z0-9]+)|(,)"
        
        matches = re.findall(REGEX_PATTERN, logic)
        
        # Iterate through matches
        for match in matches:
            
            # If the first element of the is present then we have a POS or another special constant, so try to match it back
            if(match[0]) :
                token = match[0].strip()
                if(token in word_dict) :
                    token_to_output = word_dict[token].capitalize()
                else:
                    token_to_output = token

            # Else not present - we don't have a POS, so just search for the first element of the match which
            # is present and output that
            else:
                for token in match:
                    if(token):
                        token_to_output = token
                        break
                
            generated_logic_sequence.append(token_to_output)
        
        
        
        # Output the logic sequence
        prev_token = ""
        for logic_token in generated_logic_sequence :
            
            if not logic_token in logic_vocab_this_file:
                logic_vocab_this_file[logic_token] = True
            
            # Make sure each token is separated from the previous one with a space
            if prev_token:
                if( (not prev_token.endswith(" ")) and (not prev_token.endswith("\t"))):
                    out_file_tgt.write(" ")
            
            out_file_tgt.write(logic_token)
            
            prev_token = logic_token
            
        # Finish the logic line with a newline
        out_file_tgt.write('\n')
        
    print(f"Language vocab size : {len(language_vocab_this_file)}")
    print(f"Logic vocab size : {len(logic_vocab_this_file)}")
        
generate_data(ENGLISH_TRAIN, LOGIC_TRAIN, TRAIN_COUNT)
generate_data(ENGLISH_VAL, LOGIC_VAL, VAL_COUNT)
generate_data(ENGLISH_TEST, LOGIC_TEST, VAL_COUNT)

print("DONE!")
    
