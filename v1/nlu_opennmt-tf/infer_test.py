import os
import argparse

import tensorflow as tf
import opennmt as onmt

from opennmt import constants
from opennmt.utils import decay
from opennmt.utils import losses
from opennmt.utils import misc
from opennmt.utils import optim

mode = tf.estimator.ModeKeys.PREDICT

EXPORT_DIR = "C:\\Users\\LeeBorlace\\Documents\\GitHub\\logic-ml-bot\\v1\\nlu_opennmt-tf\\run\\export\\latest\\1569615087"

with tf.Session() as sess:
    meta_graph_def = tf.saved_model.loader.load(
        sess, [tf.saved_model.tag_constants.SERVING], EXPORT_DIR)
    
    signature_def = meta_graph_def.signature_def["serving_default"]

    input_tokens = signature_def.inputs["tokens"].name
    input_length = signature_def.inputs["length"].name
    output_tokens = signature_def.outputs["tokens"].name
    output_length = signature_def.outputs["length"].name

    while True:
        text = input("Input>")
        
        if(text == "\exit" or text == "\quit"):
            break
        
        split = text.split(' ')

        inputs = {
            input_tokens: [
                split],
            input_length: [len(split)]
        }
    
        batch_tokens, batch_length = sess.run(
            [output_tokens, output_length], feed_dict=inputs)
    
        for tokens, length in zip(batch_tokens, batch_length):
            tokens, length = tokens[0], length[0]  # Take the best hypothesis.
            length -= 1  # Ignore </s> token.
            
            token_list = tokens[:length].tolist()
            translation=""
            for token in token_list:
                translation += token.decode("utf-8") + " "
                
            translation = translation.strip()
           
            print(translation)
        
        
