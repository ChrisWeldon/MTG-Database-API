from datetime import date
from datetime import datetime
import json
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

    Event class is used to represent one event from MTG Goldfish. The Events class acts as a model for one row in a MySQL database.

    Attributes:
        event_url: A string of format "/tournament/<int number>". This is a relative url on www.mtggoldfish.com.
        decks: An array if deck id's from mtggoldfish.com. Represntative of the decks that placed in the event.
        date: A date object at the day the event occured.
        id: An int pulled from event_url as a unique id for the event.
        format: A str representation of format. 'standard','pioneer','modern'
    """

    def __init__(self, event_url, decks=[], id=-1, date="", format=None):
        """Inits Event with an event url"""
        self.event_url = event_url
        self.decks = decks
        self.date = date
        self.id = id
        self.format = format
        if id==-1 and event_url:
            self.id = int(event_url.split('/')[-1])

    def __str__(self):
        """Converts to printable string"""
        #return self.event_url +" : "+ datetime.strftime(self.date, "%Y-%m-%d")
        return self.event_url +" : "+ self.date

    def __eq__(self, o):
        """Overides == operator : compares based on Event.id"""
        return isinstance(o, Event) and self.id == o.id

    def __repr__(self):
        object = {
            "id":self.id,
            "event_url" :self.event_url,
            "format": self.format,
            "date": datetime.strftime(self.date, "%Y-%m-%d"),
            "decks": self.decks,
        }
        return object

    def getEventURL(self):
        """Deprecated: Getter for event_url"""
        return self.event_url

    def getDecks(self):
        """Deprecated: Getter for decks"""
        return self.decks

    def isEmpty(self):
        """Returns Status of empty"""
        return len(self.decks) == 0;

    def getDate(self):
        """Gives string representation of date"""
        return datetime.strptime(self.date, "%Y-%m-%d").date()
        #return self.date

    def setDecks(self, decks):
        """Deprecated: Setter of decks"""
        self.decks = decks

    def addDeck(self, deck):
        """Adds deck to decks"""
        self.decks.append(deck);
        return deck

    def getID(self):
        """Deprecated: Getter of id"""
        return self.id

    def setOcc(self, occ):
        """Deprecated: setter of occ"""
        self.occ = occ

    def getOcc(self):
        """Deprecated: getter of occ"""
        return self.occ

    def setCardOccurances(self, cards):
        """Deprecated: setter of occurance objects"""
        self.card_occurances = cards

    def addCardOccurance(self, card_occurance):
        """Deprecated: adds one occurance to occurance objects"""
        if(card_occurance not in self.card_occurances):
            self.card_occurances.append(card_occurance)
            return True
        return False

    def getCardOccurances(self):
        """Deprecated: getter of card_occurances"""
        return self.card_occurances
