from flask import Flask, jsonify, g
import sys, os, json
from mtgapi.common.Card import Card
from mtgapi.common.Database import Database
from mtgapi.common.CardPrice import CardPrice
from mtgapi.common.CardOccurance import CardOccurance
from mtgapi.common.Event import Event
from flask import url_for, redirect, abort
import pandas as pd

app = Flask(__name__)
cpath = 'mtgapi/config_api.json'

def get_db():
    if 'db' not in g:
        g.db = Database(path=cpath)
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        del(db)

@app.route('/')
def hello_world():
    return '''<p>API for Magic the Gathering occurance data in tournaments. The documentation can be found on <a href="https://github.com/ChrisWeldon/MTG-Database-API">Github</a>.
                Visit <a href="/about">about</a> for license.</p>'''

@app.route('/about')
def get_about():
    return redirect(url_for('static', filename='LICENSE_web'))

@app.route('/card/<card_name>')
def get_card(card_name):
    db = get_db()
    card = db.getCardByTitle(card_name)
    if(card==False):
        return "Card Does not exist"

    return json.dumps(card.__repr__())

@app.route('/cards/')
def get_cards():
    db = get_db()
    cards = db.getCards()
    repr_cards = []
    for c in cards:
        repr_cards.append(c.__repr__())
    return json.dumps(repr_cards)

@app.route('/events/')
def get_events():
    db = get_db()
    events = db.getEvents()
    repr_events = []
    for e in events:
        repr_events.append(e.__repr__())
    return json.dumps(repr_events)

@app.route('/plays/<card_name>')
def get_plays(card_name):
    db = get_db()
    card = db.getCardByTitle(card_name)
    if(card==False):
        return "Card Does not exist"
    plays = db.getOccurancesByCard(card)

    repr_plays = []
    for p in plays:
        repr_plays.append(p.__repr__())

    return json.dumps(repr_plays)



@app.route('/df/plays/<card_id>/<format>')
def get_dfplays(card_id, format):

    def max_decks(num):
            if num>16:
                return 16
            else:
                return num

    if(format=="None"):
        format = None
    db = get_db()
    card = db.getCardByID(card_id)
    if(card==False):
        return "Card Does not exist"

    plays = db.getCardSeriesDataFrame(card, format=format)
    plays['deck_nums'] = plays['deck_nums'].apply(max_decks)

    events = db.getTournamentSeriesDataFrame(format=format)
    events = events.set_index('date').groupby('date').min()
    format_occ = plays[['date', 'tot_occ', 'deck_nums']].set_index('date').groupby('date').sum()
    format_occ['norm_occ']  = format_occ['tot_occ']/format_occ['deck_nums']

    occ_series = pd.merge(events, format_occ, how='left', left_index=True, right_index=True).fillna(0)
    occ_series = occ_series.drop(['url','format','id'], axis=1)

    return occ_series.to_json(orient='columns')

@app.route('/df/plays/<card_id>/')
def get_dfplays_none(card_id):
    return redirect(url_for('get_dfplays', card_id=card_id, format='None'))


@app.route('/search/<type>/<string>')
def search(type, string):
    db = get_db()
    if(type=="cards"):
        results = db.searchCards(string)
    else:
        abort(404)

    repr_results =[]
    for r in results:
        repr_results.append(r.__repr__())
    return json.dumps(repr_results)


if __name__=="__main__":
    app.run(host='0.0.0.0')
