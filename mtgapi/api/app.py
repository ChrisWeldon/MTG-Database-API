from flask import Flask, jsonify
import sys, os, json
sys.path.insert(0, "/var/www/MTG_Database/mtgapi")
from mtgapi.common.Card import Card
from mtgapi.common.Database import Database
from mtgapi.common.CardPrice import CardPrice
from mtgapi.common.CardOccurance import CardOccurance
from mtgapi.common.Event import Event

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'API for Magic the Gathering occurance data in tournaments.'

@app.route('/card/<card_name>')
def get_card(card_name):
    db = Database(path='config_api.json')
    card = db.getCardByTitle(card_name)
    if(card==False):
        return "Card Does not exist"

    return json.dumps(card.__repr__())

@app.route('/plays/<card_name>')
def get_plays(card_name):
    db = Database(path='config_api.json')
    card = db.getCardByTitle(card_name)
    if(card==False):
        return "Card Does not exist"

    plays = db.getOccurancesByCard(card)

    repr_plays = []
    for p in plays:
        repr_plays.append(p.__repr__())

    return json.dumps(repr_plays)
