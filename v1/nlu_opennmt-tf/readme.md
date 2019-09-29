# Intro
This folder is for doing a test of english > logic via opennmt-tf

# Info
http://opennmt.net/OpenNMT-tf/quickstart.html
https://github.com/OpenNMT/Tokenizer/blob/master/docs/options.md

# Generating training data
`python ..\nlu_training_data_generator\generate_train_data.py 500000 0.7 0.15 0.15 0.0001 0.0001 0.00001 C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\nlu_training_data_generator\vocab.json C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\nlu_training_data_generator\training_templates.json`

`onmt-build-vocab --size 50000 --save_vocab src-vocab.txt src-train.txt`
`onmt-build-vocab --size 50000 --save_vocab tgt-vocab.txt tgt-train.txt`

# Training (small)
`onmt-main train_and_eval --model_type NMTSmall --auto_config --config NMTSmall.yml`
`tensorboard --logdir="run"` - have to hit at localhost:6006

# Training (Transformer)
`onmt-main train_and_eval --model_type Transformer --auto_config --config Transformer.yml`
`tensorboard --logdir="run"` - have to hit at localhost:6006


# Inferring
`python infer.py C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\nlu_opennmt-tf\run\export\latest\1569615087`
`python infer.py C:\Users\LeeBorlace\Documents\GitHub\logic-ml-bot\v1\nlu_opennmt-tf\run\export\latest\1569734247`

# Export issue
Was getting this in the process :
`tensorflow.python.framework.errors_impl.NotFoundError: Failed to create a directory: run/export\latest\temp-b'1569242016'; No such file or directory`

Seems to be fixed by using `model_dir: run` instead of `model_dir: run\` in data.yml

