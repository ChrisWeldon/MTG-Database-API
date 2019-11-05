import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src.Database import Database
from src.Card import Card
from src.DataCollector import DataCollector
from src.Inventory import Inventory

def update_collection():
    dc = DataCollector()
    db = Database()
    core = dc.get_cards_in_set("/set/M20/core-set-2020/", rarities=['mythic-rare'])
    db.addCardsToCollection(core)

if __name__ == "__main__":
    update_collection()
