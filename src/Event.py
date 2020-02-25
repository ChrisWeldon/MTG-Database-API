class Event:

    def __init__(self, event_url, decks=[], id=-1, date=""):
        self.event_url = event_url
        self.decks = decks
        self.date = date
        self.id = id
        if id==-1 and event_url:
            self.id = int(event_url.split('/')[-1])

    def __str__(self):
        return self.event_url +" : "+self.date + " - " + str(len(self.decks)) + " Decks"

    def __eq__(self, o):
        return isinstance(o, Event) and self.id == o.getID()

    def getEventURL(self):
        return self.event_url

    def getDecks(self):
        return self.decks

    def isEmpty(self):
        return len(self.decks) == 0;

    def getDate(self):
        return self.date

    def setDecks(self, decks):
        self.decks = decks

    def addDeck(self, deck):
        self.decks.append(deck);
        return deck

    def getID(self):
        return self.id
