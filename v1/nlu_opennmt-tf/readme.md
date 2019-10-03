# Info
http://opennmt.net/OpenNMT-tf/quickstart.html
https://github.com/OpenNMT/Tokenizer/blob/master/docs/options.md

# English to logic training
## Generating training data
`python ..\nlu_training_data_generator\generate_train_data.py 500000 0.7 0.15 0.15 0.0001 0.0001 0.00001 C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\nlu_training_data_generator\vocab.json C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\nlu_training_data_generator\training_templates.json 0.75`

`onmt-build-vocab --size 50000 --save_vocab english-vocab.txt english-train.txt`
`onmt-build-vocab --size 50000 --save_vocab logic-vocab.txt logic-train.txt`

## Training (small)
`onmt-main train_and_eval --model_type NMTSmall --auto_config --config NMTSmall_eng_logic.yml`
`tensorboard --logdir="run"` - have to hit at localhost:6006

## Training (Transformer)
`onmt-main train_and_eval --model_type Transformer --auto_config --config Transformer_eng_logic.yml`
`tensorboard --logdir="run"` - have to hit at localhost:6006

# Logic to English training
## Generating training data
`python ..\nlu_training_data_generator\generate_train_data.py 500000 0.7 0.15 0.15 0.0001 0.0001 0.00001 C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\nlu_training_data_generator\vocab.json C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\nlu_training_data_generator\training_templates.json 0.75`

`onmt-build-vocab --size 28746 --save_vocab english-vocab.txt english-train.txt`
`onmt-build-vocab --size 26265 --save_vocab logic-vocab.txt logic-train.txt`

## Training (small)
`onmt-main train_and_eval --model_type NMTSmall --auto_config --config NMTSmall_logic_eng.yml`
`tensorboard --logdir="run"` - have to hit at localhost:6006

## Training (Transformer)
`onmt-main train_and_eval --model_type Transformer --auto_config --config Transformer_logic_eng.yml`
`tensorboard --logdir="run"` - have to hit at localhost:6006

# Inferring (using latest export)
`python infer.py`