import mysql.connector
from mysql.connector.errors import *
import sys, json, os, math, datetime
import numpy as np
import pandas as pd

from .Card import Card
from .CardPrice import CardPrice
from .Event import Event
from .CardOccurance import CardOccurance
from .DatatypeExceptions import DatePricingError

"""A Module containing the Database Class

The Database Object used to interact with a MySQL database.


    Terms:
        format:
    Typical usage example:

    from Data import Database #or if outside package
    from src import Database

    db = Database()
    card = db.getCardByTitle("Blue Eyes White Dragon")
    db.addCard(card)

"""
class Database:
    """A Class for the Database object

    Database is used as an object which interacts with a MySQL database. Check GITHUB page for schema details on MySQL database.

    Attributes:
        config: path to file containing database connection information
        cnx: a mysql-connector connection.

    """
    def __init__(self, path = '../config.json'):
        """Inits Database with specified config file. On reading of config

        Args:
            path: a string '/path/to/config.json'

        """
        try:
            with open(path, 'r') as json_file:
                text = json_file.read()
                json_data = json.loads(text)
                self.config = json_data
            self.cnx = mysql.connector.connect(user=self.config["database"]["user"], password=self.config["database"]["password"],
                                          host=self.config["database"]["host"],
                                          database= (self.config["database"]["dev_database_name"] if self.config["dev"]=="True" else self.config["database"]["database_name"]),
                                          use_pure=self.config['database']['use_pure']=="True")

        except Exception as e:
            # TODO: throw custom exception for error on initial
            print(e)
            print("Config File Not Found!");
            self.cnx = None
            self.config = None

    def __del__(self):
        """Closes cnx connection"""
        self.cnx.close()

    def isConnected(self):
        """Returns if connection is connected"""
        if(self.cnx != None):
            return True
        else:
            return False

    def addCard(self, card):
        # TODO: upload release date too
        """Adds Card Model to Database.

        Args:
            card: A Card object which contains title, set, echo_id, and release_date.

        """
        cursor = self.cnx.cursor()
        insert_card = ("INSERT INTO cards"
                        """(title,set_mtg, echo_id, rarity)"""
                        "VALUES (%s, %s, %s, %s)")
        insert_card_data = (card.title, card.set, card.echo_id, card.rarity)
        try:
            cursor.execute(insert_card, insert_card_data)
            self.cnx.commit()
        except Exception as err:
            print(err)
            return False
        id = cursor.lastrowid
        return id

    def addCards(self, cards):
        """Adds list of Cards to database using addCard()

        Args:
            cards: an array of cards.
        """
        for card in cards:
            self.addCard(card)
            print(str(card.echo_id) + " - " + card.title)

    def getCards(self, from_date= datetime.date(2017, 9, 28)):
        """Retrieves all cards in the Cards table.

        Returns:
            Array of Card objects.
        """
        cursor = self.cnx.cursor()
        query = ("SELECT * FROM `cards` "
                " WHERE rotation_date is NULL OR rotation_date >= %s ")
        vals = (from_date,)
        cursor.execute(query,vals)
        cards = []
        for row in cursor.fetchall():
            cards.append(Card(title=row[0],set = row[1], echo_id = row[5], rarity=row[4], release_date=row[2], rotation_date=row[3]))
        return cards

    def getCardByTitle(self, title, date=datetime.date.today()):
        # RESOLVE: What happens when there is no card by this name?
        """Retrieves one card from the database by title.

        Retrieves a card from the cards table. If multiple cards are queried (IE two of the same card from different
        sets) then the date arg is used to reconcile which age of card is required. The most recent version available
        is always returned.

        For example:
            Sorcerous Spyglass returns two cards, one from Ixilan and Eldrain. By passing in a date (date of event) we can further
            filter our results. If the event occured before the release of Eldrain then the Ixilan version is return.

        Args:
            title: a string of the title of the desired card.
            date: a datetime object to resolve multiple cards of the same name.

        Returns:
            A Card object.
        """
        cursor = self.cnx.cursor()
        query = ("SELECT * FROM `cards` WHERE `title` = %s AND `release_date` <= %s ORDER BY `release_date` DESC")
        values = (title, date)
        try:
            cursor.execute(query, values)
        except Exception as err:
            print(err)
            return False

        try:
            data = cursor.fetchall()[0]
        except IndexError:
            return False

        return Card(title=data[0], set=data[1], echo_id=data[5], rarity=data[4], release_date=data[2])

    def getCardByID(self, id, date=datetime.date.today()):
        """Retrieves one card from the database by ECHO ID.

        Retrieves a card from the cards table. If multiple cards are queried (IE two of the same card from different
        sets) then the date arg is used to reconcile which age of card is required. The most recent version available
        is always returned.

        For example:
            Sorcerous Spyglass returns two cards, one from Ixilan and Eldrain. By passing in a date (date of event) we can further
            filter our results. If the event occured before the release of Eldrain then the Ixilan version is return.

        Args:
            title: a string of the title of the desired card.
            date: a datetime object to resolve multiple cards of the same name.

        Returns:
            A Card object.
        """
        cursor = self.cnx.cursor()
        query = ("SELECT * FROM `cards` WHERE `echo_id` = %s AND `release_date` <= %s ORDER BY `release_date` DESC")
        values = (id, date)
        try:
            cursor.execute(query, values)
        except Exception as err:
            print(err)
            return False

        try:
            data = cursor.fetchall()[0]
        except IndexError:
            return False

        return Card(title=data[0], set=data[1], echo_id=data[5], rarity=data[4], release_date=data[2])

    def addEvent(self, event):
        """Adds Event object to database

        Args:
            event: An Event object

        Returns: A boolean, True if successful addition, False if failed.
        """
        cursor = self.cnx.cursor()
        insert_tournament = ("INSERT INTO tournaments"
                            """(date, url, format, id)"""
                            "VALUES (%s, %s, %s, %s)")
        insert_values = (event.date, event.event_url, event.format, event.id)
        try:
            cursor.execute(insert_tournament, insert_values)
            self.cnx.commit()
        except Exception as err:
            print(err)
            return False
        return True

    def addEvents(self, events):
        """Adds list of Event objects using addEvent()"""
        for event in events:
            self.addEvent(event)
        return True

    def getLastTimelineDate(self):
        """Deprecated: Retrieves the date of the occurance collected

        This method is useful for when there is weekly/daily collection so a script can pickup where it left off.

        Returns:
            A datetime date object.
        """
        cursor = self.cnx.cursor()
        query = ("""SELECT MAX(date) FROM `card_series`;""")
        try:
            cursor.execute(query)
        except Exception as err:
            print(err)
            return False

        for row in cursor.fetchall():
            if row[0]==None:
                return False
            return row[0]
        return False

    def getLastEventDate(self, format=None):
        """Retrieves the date of the event collected

        This method is useful for when there is weekly/daily collection so a script can pickup where it left off.

        Returns:
            A datetime date object.
        """
        cursor = self.cnx.cursor()
        query = ("""SELECT MAX(date) FROM `tournaments`;""")
        if format!= None:
            query = ("SELECT MAX(date) FROM `tournaments` WHERE `format` = '"+format+"';")
        try:
            cursor.execute(query)
        except Exception as err:
            print(err)
            return False

        for row in cursor.fetchall():
            if row[0]==None:
                return False
            return row[0]
        return False

    def addCardOccurance(self, play):
        """Adds a CardOccurance Object to the Database

        Args:
            play: A CardOccurance object
        """
        assert isinstance(play, CardOccurance), "Expected instance of CardOccurance, got " + str(play)

        cursor = self.cnx.cursor()
        insert = ("INSERT INTO card_series"
                        """(rowid, title,date,tot_occ,event_,format,deck_nums,
                        first_place,secon_place,third_place,fourt_place,
                        fifth_place,sixth_place,seven_place,eigth_place,
                        ninet_place,tenth_place,twelt_place,thtee_place,
                        fotee_place,fitee_place,sitee_place,nineo,eighto,
                        seveno,sixo,fiveo,sixone,fivetwo,eightone,seventwo,
                        sevenone,sixtwo,echo_id)"""
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s)")

        occ = {
            'raw':0,
            '1st Place':0,
            '2nd Place':0,
            '3rd Place':0,
            '4th Place':0,
            '5th Place':0,
            '6th Place':0,
            '7th Place':0,
            '8th Place':0,
            '9th Place':0,
            '10th Place':0,
            '11th Place':0,
            '12th Place':0,
            '13th Place':0,
            '14th Place':0,
            '15th Place':0,
            '16th Place':0,
            '(9-0)': 0,
            '(8-0)': 0,
            '(7-0)': 0,
            '(6-0)': 0,
            '(5-0)': 0,
            '(6-1)': 0,
            '(5-2)': 0,
            '(8-1)': 0,
            '(7-2)': 0,
            '(7-1)': 0,
            '(6-2)': 0
        }
        data = play.occ
        occ.update(data)
        insert_data = (play.id, play.card.title, play.date, occ['raw'], str(play.event.event_url),play.format, len(play.event.decks) , occ['1st Place'],
                                occ['2nd Place'], occ['3rd Place'], occ['5th Place'], occ['6th Place'], occ['7th Place'], occ['8th Place'],
                                occ['9th Place'], occ['10th Place'], occ['11th Place'], occ['12th Place'], occ['13th Place'], occ['14th Place'],
                                occ['15th Place'], occ['16th Place'],occ['(9-0)'],occ['(8-0)'],occ['(7-0)'],occ['(6-0)'],occ['(5-0)'],
                                occ['(6-1)'],occ['(5-2)'],occ['(8-1)'],occ['(7-2)'],occ['(7-1)'],occ['(6-2)'],play.card.echo_id)

        try:
            cursor.execute(insert, insert_data)
        except IntegrityError as err:
            print(err)
            return False
        self.cnx.commit()

    def addCardPrice(self, cardprice):
        """ Adds CardPrice object to the database.

        Args:
            cardprice: An instance of a CardPrice object to be serialized and added.

        Returns:
            A boolean describing success of database addition.
        """

        assert isinstance(cardprice, CardPrice), "Expected instance of CardPrice, got " + str(play)

        cursor = self.cnx.cursor()
        insert = ("INSERT INTO price_series"
                """(date, title, price, tix, rowid, echo_id)"""
                "VALUES (%s, %s, %s, %s, %s, %s)")
        rowid= str(cardprice.card.echo_id) + ":" + str(cardprice.date)
        cpp = float(cardprice.price) if cardprice.price != None else None
        cpt = float(cardprice.tix) if cardprice.tix != None else None
        insert_data = (cardprice.date, cardprice.card.title, cpp, cpt, rowid, cardprice.card.echo_id)

        try:
            cursor.execute(insert, insert_data)
        except IntegrityError as err:
            print(err)
            return False
        self.cnx.commit()
        return True

    def addCardPrices(self, cardprices):
        """ Adds and array of cardprices"""
        for p in cardprices:
            self.addCardPrice(p)

    def getCardPriceByDate(self, card, date):
        """ Retrieves a the price of a card at a specific date

        Args:
            card: Card object containing data about the desired card price.
            date: datetime of the desired price.
        """

        cursor = self.cnx.cursor(dictionary=True)
        query = ("SELECT * FROM `price_series` WHERE `title` = %s AND `date` = %s")
        data = (card.title, date)
        cursor.execute(query, data)
        return cursor.fetchone()

    def getOccurancesByCard(self, card):
        """Retrieves a list of CardOccurance in database based on card"""

        cursor = self.cnx.cursor(dictionary=True)
        query = ("SELECT * FROM `card_series` WHERE `title` = '"+card.title+"' ORDER BY `date` DESC")
        cursor.execute(query)

        plays = []
        for p in cursor.fetchall():
            # Building the the Objects that CardOccurance wraps around
            event = Event(event_url=p['event_'], format=p['format'], date=p['date'])

            #Creating a subset of the result to become the CardOccurance.occ attribute
            tuple_not_in_occ = ('title', 'date', 'price', 'tix', 'event_', 'format', 'echo_id', 'rowid');
            occ = {k: p[k] for k in p.keys() if k not in tuple_not_in_occ}

            plays.append(CardOccurance(card, event, occ=occ))

        return plays

    def getCardSeriesDataFrame(self, card, format=None):
        """ Returns a pandas dataframe of card plays by card"""
        cursor = self.cnx.cursor(dictionary=True)

        if format != None:
            query = ("SELECT * FROM `card_series` WHERE `title` = '"+card.title+"' AND `format`='"+format+"' ORDER BY `date` DESC")
        else:
            query = ("SELECT * FROM `card_series` WHERE `title` = '"+card.title+"' ORDER BY `date` DESC")

        cursor.execute(query)

        return pd.DataFrame(cursor.fetchall())

    def getPriceSeriesDataFrame(self, card):
        """ Returns a pandas dataframe of prices by card"""
        cursor = self.cnx.cursor(dictionary=True)

        query = ("SELECT * FROM `price_series` WHERE `title` = '"+card.title+"' ORDER BY `date` ASC")

        cursor.execute(query)

        return pd.DataFrame(cursor.fetchall())

    def getTournamentSeriesDataFrame(self, format=None):
        """ Returns a pandas dataframe of all events based on MTG event format"""
        cursor = self.cnx.cursor(dictionary=True)

        if format != None:
            query = ("SELECT * FROM `tournaments` WHERE `format`='"+format+"' ORDER BY `date` DESC")
        else:
            query = ("SELECT * FROM `tournaments` WHERE 1 ORDER BY `date` DESC")

        cursor.execute(query)

        return pd.DataFrame(cursor.fetchall())

    def eventCollected(self, event):
        """Checks if event has been collected"""
        cursor = self.cnx.cursor()


        query = ("SELECT COUNT(1) FROM `tournaments` WHERE `id` = "+str(event.id))
        cursor.execute(query)

        if cursor.fetchone()[0] == 0:
            return False
        return True

    def allPlaysRecorded(self, card):
        """ Returns boolean if all plays for a card have been recorded into the database"""
        play_count_query = ('SELECT COUNT(*) FROM `card_series` WHERE `title` =  "'+card.title+'"')
        event_count_query = ('SELECT COUNT(*) FROM `tournaments` WHERE `date` >= "'+datetime.datetime.strftime(card.release_date, '%Y-%m-%d') +'"')

        cursor = self.cnx.cursor()
        cursor.execute(play_count_query)
        play_count = cursor.fetchone()[0]

        cursor = self.cnx.cursor()
        cursor.execute(event_count_query)
        event_count = cursor.fetchone()[0]

        if(play_count>event_count):
            print("WARNING play count > event_count!!!!")
        return(play_count >= event_count)

    def getLastCardPriceByCard(self, card):
        """ Returns last price collected for card"""
        query = ('SELECT max(`date`) FROM `price_series` WHERE `title` = "'+card.title+'"')
        cursor = self.cnx.cursor()
        cursor.execute(query)
        result = cursor.fetchone()[0]
        return result if result != None else None

    def searchCards(self, string):

        query = ('SELECT * FROM `cards` WHERE `title` LIKE "%'+string+'%"')
        cursor = self.cnx.cursor()
        cursor.execute(query)
        cards =[]
        for row in cursor.fetchall():
            cards.append(Card(title=row[0],set = row[1], echo_id = row[5], rarity=row[4], release_date=row[2], rotation_date=row[3]))
        return cards

    def searchDate(self, string):
        cursor = self.cnx.cursor(dictionary=True)
        query = ("SELECT * FROM `card_series` WHERE `date` = '"+string+"' ORDER BY `date` DESC")
        cursor.execute(query)

        plays = []
        for p in cursor.fetchall():
            # Building the the Objects that CardOccurance wraps around
            event = Event(event_url=p['event_'], format=p['format'], date=p['date'])

            #Creating a subset of the result to become the CardOccurance.occ attribute
            tuple_not_in_occ = ('title', 'date', 'price', 'tix', 'event_', 'format', 'echo_id', 'rowid');
            occ = {k: p[k] for k in p.keys() if k not in tuple_not_in_occ}

            #TODO append occurance

        return plays
