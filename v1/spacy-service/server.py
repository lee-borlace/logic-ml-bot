from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import spacy

MODEL = "en_core_web_sm"
# MODEL = "en_core_web_lg"

nlp = spacy.load(MODEL)

app = Flask(__name__)
api = Api(app)

class Analyse(Resource):
    def get(self, input):
        doc = nlp(input)
        return [{'text':token.text,'lemma':token.lemma_,'pos':token.pos_,'tag':token.tag_} for token in doc]
        

api.add_resource(Analyse, '/analyse/<input>')

if __name__ == '__main__':
     app.run(port='5002')