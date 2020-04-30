
from Database import Database
import os
from Card import Card

class LocalDBUploader:

    def __init__(self, local_path = "../data/"):
        self.db = Database();
        self.cards = []
        self.local_path = local_path


    def getAllCards(self):
        for (dirpath, dirnames, filenames) in os.walk(self.local_path):
            for filename in filenames:
                if filename == 'manifest.csv':
                    print(dirpath)
                    self.cards.append(Card(manifest_path=os.path.join(dirpath, filename), price_data_path=os.path.join(dirpath, 'historic.csv'), occ_data_path="../data/occurance_data-1.csv"))
        return self.cards


if __name__ == "__main__":
    db = Database()
    script = LocalDBUploader()
    cards = script.getAllCards()
    for card in cards:
        if card.rarity == "mythic-rare" or card.rarity == "rare":
            print(card.rarity)
            card.assembleTimeline()
            #db.addCardToCollecton(card)
            db.uploadCardTimeline(card)
