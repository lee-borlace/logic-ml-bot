import json

NUM_SAMPLES = 100

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
        
generate_data(SRC_TRAIN, TGT_TRAIN, TRAIN_COUNT)
generate_data(SRC_VAL, TGT_VAL, VAL_COUNT)
    
