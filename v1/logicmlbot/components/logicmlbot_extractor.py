from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata

import os

import typing
from typing import Any, Optional, Text, Dict

SENTIMENT_MODEL_FILE_NAME = "sentiment_classifier.pkl"

class LogicMlBotExtractor(Component):
    """A custom sentiment analysis component"""
    name = "sentiment"
    provides = ["entities"]
    requires = ["tokens"]
    defaults = {}
    language_list = ["en"]
    print('initialised the class')

    def __init__(self, component_config=None):
        super(LogicMlBotExtractor, self).__init__(component_config)

    def train(self, training_data, cfg, **kwargs):
        """Load the sentiment polarity labels from the text
           file, retrieve training tokens and after formatting
           data train the classifier."""

        pass



    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""

        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "fol",
                  "extractor": "sentiment_extractor"}

        return entity
    

    def process(self, message, **kwargs):
        """Retrieve the tokens of the new message, pass it to the classifier
            and append prediction results to the message class."""
      
        entity = self.convert_to_rasa("instanceOf(x,Blah)", 0.666)
        message.set("fol", [entity], add_to_output=True)

    def persist(self, file_name, model_dir):
        pass