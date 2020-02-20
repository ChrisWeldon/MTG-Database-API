



class Event:

    def __init__(self, event_url, decks=[], date=None):
        self.event_url = event_url
        self.decks = decks
        self.date = date

    def __str__(self):
        return self.event_url +" : "+self.date + " - " + str(len(self.decks)) + " Decks"

    def getEventURL(self):
        return self.event_url

    def getDecks(self):
        return self.decks

    def getDate(self):
        return self.date

    def setDecks(self, decks):
        self.decks = decks

    def addDeck(self, deck):
        self.decks.append(deck);
        return deck
