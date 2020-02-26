"""A module containing the Event datatype definition.

The Event class/model representation of an mtg tournement.

    Typical usage example:

    from Event import Event #or if outside package
    from src import Event

    e = Event("/tournament/123456", decks = [1234,2345,3456])
    e.getID() #123456
    Database().addEvent(e)
"""

class Event:
    """Event Datatype

    Event class is used to represent one event from MTG Goldfish.

    Attributes:
        event_url: A string of format "/tournament/<int number>". This is a relative url on www.mtggoldfish.com.
        decks: An array if deck id's from mtggoldfish.com. Represntative of the decks that placed in the event.
        date: A date object at the day the event occured.
        id: An int pulled from event_url as a unique id for the event.
    """

    def __init__(self, event_url, decks=None, id=-1, date=""):
        self.event_url = event_url
        self.decks = decks
        self.date = date
        self.id = id
        if id==-1 and event_url:
            self.id = int(event_url.split('/')[-1])

    def __str__(self):
        return self.event_url +" : "+self.date

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

    def setOcc(self, occ):
        self.occ = occ

    def getOcc(self):
        return self.occ

    def setCardOccurances(self, cards):
        self.card_occurances = cards

    def addCardOccurance(self, card_occurance):
        if(card_occurance not in self.card_occurances):
            self.card_occurances.append(card_occurance)
            return True
        return False

    def getCardOccurances(self):
        return self.card_occurances
