#!/usr/bin/env python3
from datetime import date

"""A module containing the CardOccurance datatype definition.

The CardPrice class/model representation of a card's price at one day.

    Typical Usage Example:

    # TODO
"""

class CardPrice:

    """CardPrice Datatype

    The CardPrice datatype is used as a wrapper class of the Card datatype.
    CardPrice holds a card as well as a date for when the card was at that price.
    Unlike Card, CardPrice's price and tix attribute is a float, instead of a dataframe.
    This is because the price of a CardPrice's price  coorelates to the price of the
    associated card at the date it was played.

    Attributes:
        card: As Card object representing the associated card of the card Occurance.
        date: A datetime object of the play date.
        id: A string as a unique row identifier for a MySQL database of form '<card.echo_id>:<date>'
        price: A float of the paper cost of the card the day of the event.
        tix. A float of the MTGO cost of the card the day of the event.
    """
    def __init__(self, card, date, price=None, tix=None):
        self.card = card
        self.date = date
        if price==None:
            try:
                self.price = self.card.price.loc[self.date]['price']
            except KeyError as e:
                print(e)
                print("Price at date : ", self.date, " unavailable.")
                self.price=None

        if tix ==None:
            try:
                self.tix = self.card.tix.loc[self.date]['price']
            except KeyError as e:
                print(e)
                print("tix at date : ", self.date, " unavailable.")
                self.tix=None

        if self.price==None and self.tix==None:
            print(date)
            raise DatePricingError("No Pricing History")

try:
    from DatatypeExceptions import *
except:
    from src.DatatypeExceptions import *
