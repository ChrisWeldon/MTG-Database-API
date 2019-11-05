## This is a main process

## Collects all cards in mtg-time-series.cards and gathers all respective timelines and uploads them to database
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src.Database import Database
from src.Card import Card
from src.DataCollector import DataCollector
from src.Inventory import Inventory


def collect_timeline():
    db = Database()
    dc = DataCollector()

    global_inventory = Inventory(cards = db.getCardsInCollection())
    for card in global_inventory.getCards():
        try:
            print(str(card) + ": Downloading price data")
            dc.get_historical_prices_by_card(card) #Collect Data and get prices
        except Exception as e:
            print(e)

    # global_inventory.loadOccFromFile(file="/Users/chrisevans/Projects/MTG_Database/data/occurance_data-1.csv")
    # global_inventory.assembleTimelines()
    for card in global_inventory.getCards():

        card.loadOccFromFile(file="/Users/chrisevans/Projects/MTG_Database/data/occurance_data-1.csv")
        card.assembleTimeline()
        print(str(card))
        try:
            db.uploadCardTimeline(card)
        except Exception as e: # should be some sql error, make more specific when you figure it out uploads
            print(e)
            continue

if __name__=="__main__":
    # A one-time-use script inteded on uploading timeseries data from every card in the collection.
    collect_timeline()
