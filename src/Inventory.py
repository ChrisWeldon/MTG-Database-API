import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Inventory: A collection data type to keep track of Card objects
# Allows for operations on whole card inventories
# Cards can exist in the same inventories

class Inventory:

    def __init__(self, cards = [], name = None):
        self.cards = cards
        self.name = (name if name else "NAMELESS")

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return self.name + "<Inventory>-" + str(len(self))

    def add(self, card):
        assert isinstance(card, Card), "Expected instance of card, got " + type(card)
        self.cards.append(card)

    def remove(self, card):
        if isinstance(card, Card):
            for i in range(len(self.cards)):
                if(card==self.cards[i]):
                    return self.cards.pop(i)

        elif isinstance(card, int):
            return self.cards.pop(card)
        else:
            assert isinstance(card, Card), "Expected instance of card, got " + type(card)


    def setCards(self, cards):
        self.cards = cards

    def getCards(self):
        return self.cards

    def loadOccFromFile(self, file = ""):
        for card in self.cards:
            card.loadOccFromFile(file = file)
            if card.isEmpty() == False:
                assembleTimeline()

    def assembleTimelines(self):
        for card in self.cards:
            card.assembleTimeline()
            print(str(card))
            print(card.timeline.shape[0])
            print(card.occ.shape[0])
            print(card.price.shape[0])
            print("\n")

if __name__== "__main__":
    print("Inventory Main Called")
    from Card import Card

else:
    from src.Card import Card
