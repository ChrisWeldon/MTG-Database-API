from datetime import date
import json
from .DatatypeExceptions import DatePricingError

"""A module containing the CardOccurance datatype definition.

The CardOccurance class/model representation of an appearance of a card in an MTG event.

    Typical Usage Example:

    # TODO
"""

class CardOccurance:
    """CardOccurance Datatype

    Sometimes the name 'play' is used as a synonym for CardOccurance.

    The CardOccurance datatype is used as a wrapper class of the Card datatype.
    CardOccurance holds a card as well as a date which the occurance takes place.
    Unlike Card, CardOccurance's price and tix attribute is a float, instead of a dataframe.
    This is because the price of a CardOccurance coorelates to the price of the
    associated card at the date it was played.

    Attributes:
        card: As Card object representing the associated card of the card Occurance.
        event: An Event object representing the Event the card was played in.
        occ: A JSON object (Python Dictionary) of the occurance data.
        date: A datetime object of the play date.
        format: A string of the format of the event the card appeared in. 'pioneer', 'standard', 'modern', etc
        id: A string as a unique row identifier for a MySQL database of form '<card.echo_id>:<event.id>:<date>'
        price: A float of the paper cost of the card the day of the event.
        tix. A float of the MTGO cost of the card the day of the event.
    """
    def __init__(self, card, event, occ, date=None):
        """Initialization of the Card with Card, Event, and occ data mandatory"""
        self.card = card
        self.event = event
        self.format = event.format
        self.occ = occ
        if not date==None:
            self.date = date
        else:
            self.date = event.date
        self.id = str(card.echo_id)+ ":" + str(event.id)+ ":" + str(self.date)


    def __repr__(self):
        """ Provides a json based represenation of the CardOccurance object """

        object = {
            "event": self.event.__repr__(),
            "occ": self.occ
        }
        return object

    def __eq__(self, o):
        """Overrides the == operator to establish equality based on the card and the event"""
        isinstance(o, CardOccurance) and self.card == o.card and self.event == o.event
