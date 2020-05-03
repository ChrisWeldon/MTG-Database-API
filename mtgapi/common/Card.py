import os, csv, json, sys
import pandas as pd
import numpy as np
from datetime import timedelta, date, datetime
from .CardPrice import CardPrice
"""A module containing the Event datatype definition.

The Card class/model representation of an mtg card.

    Typical usage example:

    from Card import Card #or if outside package
    from src import Card

    c = Card(title='Blue Eyes White Dragon',set = '/url/to/set', echo_id = '1234', rarity='rare')
    c.id #1234
    Database().addCard(c)
"""

def daterange(first, last):
    dates = []
    for n in range(int ((last - first).days)+1):
        dates.append(first + timedelta(n))
    return dates

class Card:
    """Card Datatype

    The Card Class is used to represent one card in MTG. The class is also used as a Database model for one card.
    This card does not represent any particular moment in time. A card class, should represent the full extend of the card's life
    in the MTG Game given.

    This Card Class is chock full of deprecated methods and attributes. Documentation is on hold for this class
    because it needs to be completely overhauled.

    Deprecated Attributes are not incuded in Documentation.

    Attributes:
        title: A string of title of the card.
        price: A Pandas Dataframe of the paper pricing history.
        tix: A Pandas Dataframe of the MTGO pricing history
        set: A string of the URL of the set.
        echo_id: An int of the echomtg unique identifier.
        rarity: A string of the rarity of the card "rare", "mythic", "uncommon", ...
        release_date: A datetime object of the release date of the card. *Note:* Not the prerelease date. Same value as set release date.
    """
    price_data_columns =["date_unix", "datetime", "price_dollars"]
    occ_data_columns = [
        'card',
        'date',
        'date_unix',
        'raw',
        'event',
        'deck_nums',
        '1st Place',
        '2nd Place',
        '3rd Place',
        '4th Place',
        '5th Place',
        '6th Place',
        '7th Place',
        '8th Place',
        '9th Place',
        '10th Place',
        '11th Place',
        '12th Place',
        '13th Place',
        '14th Place',
        '15th Place',
        '16th Place',
        '(9-0)',
        '(8-0)',
        '(7-0)',
        '(6-0)',
        '(5-0)',
        '(6-1)',
        '(5-2)',
        '(8-1)',
        '(7-2)',
        '(7-1)',
        '(6-2)']

    def __init__(self, id=-1, title="", occ = pd.DataFrame(columns=occ_data_columns), price=pd.DataFrame(columns=['date','price']),tix=pd.DataFrame(columns=['date','price']),
                set=None,echo_id=-1,rarity=None, release_date = None, rotation_date=None):

        """Init of a card object."""
        assert isinstance(occ, pd.DataFrame), "non dataframe passed through occ"
        assert isinstance(price, pd.DataFrame), "non dataframe passed through price"
        self.id = id
        self.title = title
        self.release_date = release_date
        self.rotation_date = rotation_date
        self.occ = occ
        self.price = price
        self.tix = tix
        self.set = set
        self.echo_id = echo_id
        self.rarity = rarity

    def __repr__(self):
        object = {
            'id': self.echo_id,
            'title': self.title,
            'release_date': datetime.strftime(self.release_date, "%Y-%m-%d") if self.release_date!=None else None,
            'rotation_date': datetime.strftime(self.rotation_date, "%Y-%m-%d") if self.rotation_date!=None else None,
            'set': self.set,
            'rarity':self.rarity
        }
        return object


    def __eq__(self, o):
        """ Returns True or False based on echo_id"""
        return isinstance(o, Card) and o.echo_id == self.echo_id

    def __str__(self):
        """ Returns readable string of card.
        Important for logging and such."""
        return str(self.echo_id) + "-" + str(self.title)

    def isEmpty(self):
        """ Deprecated from other versions"""
        #TODO
        return False;

    def dateparse(time_unix):
        """ Converts unix timestamp into string"""
        return datetime.utcfromtimestamp(int(time_unix)/1000).strftime('%Y-%m-%d %H:%M:%S')

    def CardPrices(self, start=None, end=None):
        """ Returns an of array of CardPrice objects from the start and end dates.

        Args:
            start: a datetime indicating the start of desired CardPrice retrieval.
            end: a datetime indication the end of desired CardPrice retrieval
        """
        if start == None:
            start = card.release_date
        if end == None:
            end=date.today()

        prices = []
        for day in daterange(start, end):
            try:
                prices.append(CardPrice(self, day))
            except DatePricingError as e:
                print("No Price info on day ", day)
        return prices
