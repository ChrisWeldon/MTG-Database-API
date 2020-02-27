import mysql.connector
import datetime
import sys, json
import numpy as np
import pandas as pd
import math



## Important database notes
# there will be a row per card/day table
# there will be a table of all cards, ids, sets they belong to


# Database interaction Object

class Database:

    def __init__(self, path = '../config.json'):
        try:
            with open(path, 'r') as json_file:
                text = json_file.read()
                json_data = json.loads(text)
                self.config = json_data
            self.check_time_hours = 1
            self.cnx = mysql.connector.connect(user=self.config["database"]["user"], password=self.config["database"]["password"],
                                          host=self.config["database"]["host"],
                                          database= (self.config["database"]["dev_database_name"] if self.config["dev"]=="True" else self.config["database"]["database_name"]))

        except Exception as e: # TODO need to handle if config file fails and if internet fails
            print(e)
            self.cnx = None
            self.check_time_hours = 0
            self.config = None
        #li.log("DatabaseInterface Initialized")

    def __del__(self):
        self.cnx.close()

    def isConnected(self):
        if(self.cnx != None):
            return True
        else:
            return False

    # @param: Card Object with data all data.
    # @returns: boolean true if upload successful boolean false if not successful.
    def addCardTimeline(self, card):
        assert isinstance(card, Card), "Expected instance of card, got " + card

        cursor = self.cnx.cursor()
        insert_timeline = ("INSERT INTO card_series"
                        """(rowid, title,date,price,tot_occ,event_,deck_nums,
                        first_place,secon_place,third_place,fourt_place,
                        fifth_place,sixth_place,seven_place,eigth_place,
                        ninet_place,tenth_place,twelt_place,thtee_place,
                        fotee_place,fitee_place,sitee_place,nineo,eighto,
                        seveno,sixo,fiveo,sixone,fivetwo,eightone,seventwo,
                        sevenone,sixtwo,echo_id)"""
                        "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s)")

        toolbar_width = 60
        # setup toolbar
        sys.stdout.write("Uploading: ")
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1))
        if(card.timeline.shape[0]>0):
            step = toolbar_width/card.timeline.shape[0]
        else:
            step =.1
        draw_mark = 0
        for index, df_row in card.timeline.iterrows():
            draw_mark = draw_mark + step
            row = {}
            df = df_row.astype(object).where(pd.notnull(df_row), None)
            for item in df.iteritems():
                row[item[0]] = item[1]

            if draw_mark>1:
                sys.stdout.write("-")
                sys.stdout.flush()
                draw_mark = 0

            insert_timeline_data = (str(card.echo_id)+"-"+str(row['datetime']),card.title, row['datetime'], row['price'], row['raw'], None, row['deck_nums'], row['1st Place'],
                                    row['2nd Place'], row['3rd Place'], row['5th Place'], row['6th Place'], row['7th Place'], row['8th Place'],
                                    row['9th Place'], row['10th Place'], row['11th Place'], row['12th Place'], row['13th Place'], row['14th Place'],
                                    row['15th Place'], row['16th Place'],row['(9-0)'],row['(8-0)'],row['(7-0)'],row['(6-0)'],row['(5-0)'],
                                    row['(6-1)'],row['(5-2)'],row['(8-1)'],row['(7-2)'],row['(7-1)'],row['(6-2)'],card.echo_id)

            # try:
            check = ("SELECT * FROM card_series WHERE rowid = '" + str(card.echo_id)+"-"+str(row['datetime']) + "'")
            cursor.execute(check)

            if cursor.fetchone() != None:
                delete = ("DELETE FROM card_series WHERE rowid = '" + str(card.echo_id)+"-"+str(row['datetime']) + "'")
                print("EXISTS, DELETING " + str(card.echo_id)+"-"+str(row['datetime']))
                cursor.execute(delete)
                self.cnx.commit()

            cursor.execute(insert_timeline, insert_timeline_data)
            self.cnx.commit()
            # except Exception as e:
            #     print(e)
            #     continue
        sys.stdout.write("]\n")

    def addCard(self, card):
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
        for card in cards:
            self.addCard(card)
            print(str(card.echo_id) + " - " + card.title)

    def getCards(self):
        cursor = self.cnx.cursor()
        query = ("SELECT * FROM cards")
        cursor.execute(query)
        cards = []
        for row in cursor.fetchall():
            cards.append(Card(title=row[0],set = row[1], echo_id = row[5], rarity=row[4]))
        return cards

    def getCardByTitle(self, title):
        cursor = self.cnx.cursor()
        query = ('SELECT * FROM cards WHERE `title` = "' + title +'"')
        try:
            cursor.execute(query, (title))
        except Exception as err:
            print(err)
            return False

        try:
            data = cursor.fetchall()[0]
        except IndexError:
            return False

        return Card(title=data[0], set=data[1], echo_id=data[5], rarity=data[4])

    def addEvent(self, event):
        cursor = self.cnx.cursor()
        insert_tournament = ("INSERT INTO tournaments"
                            """(date, url, id)"""
                            "VALUES (%s, %s, %s)")
        insert_values = (event.getDate(), event.getEventURL(), event.getID())
        try:
            cursor.execute(insert_tournament, insert_values)
            self.cnx.commit()
        except Exception as err:
            print(err)
            return False
        return True

    def addEvents(self, events):
        for event in events:
            self.addEvent(event)
        return True

    def getEvents(self):
        cursor = self.cnx.cursor()
        query = ("SELECT * FROM tournaments")
        cursor.execute(query)
        events = []
        for row in cursor.fetchall():
            events.append(Event(row[1], id=row[2], date=row[0]))
        return events

    def getLastTimelineDate(self):
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

    def getLastEventDate(self):
        cursor = self.cnx.cursor()
        query = ("""SELECT MAX(date) FROM `tournaments`;""")
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
        assert isinstance(play, CardOccurance), "Expected instance of CardOccurance, got " + str(play)

        cursor = self.cnx.cursor()
        insert = ("INSERT INTO card_series"
                        """(rowid, title,date,price,tot_occ,event_,deck_nums,
                        first_place,secon_place,third_place,fourt_place,
                        fifth_place,sixth_place,seven_place,eigth_place,
                        ninet_place,tenth_place,twelt_place,thtee_place,
                        fotee_place,fitee_place,sitee_place,nineo,eighto,
                        seveno,sixo,fiveo,sixone,fivetwo,eightone,seventwo,
                        sevenone,sixtwo,echo_id)"""
                        "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s)")

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
        data = play.getOcc()
        occ.update(data)
        insert_data = (str(play.getCard().getID())+":"+str(play.getEvent().getID())+":"+str(play.getDate()), play.getCard().title, play.getDate(), float(play.getPrice()), occ['raw'], str(play.getEvent().getEventURL()), len(play.getEvent().getDecks()), occ['1st Place'],
                                occ['2nd Place'], occ['3rd Place'], occ['5th Place'], occ['6th Place'], occ['7th Place'], occ['8th Place'],
                                occ['9th Place'], occ['10th Place'], occ['11th Place'], occ['12th Place'], occ['13th Place'], occ['14th Place'],
                                occ['15th Place'], occ['16th Place'],occ['(9-0)'],occ['(8-0)'],occ['(7-0)'],occ['(6-0)'],occ['(5-0)'],
                                occ['(6-1)'],occ['(5-2)'],occ['(8-1)'],occ['(7-2)'],occ['(7-1)'],occ['(6-2)'],play.getCard().getID())

        cursor.execute(insert, insert_data)
        self.cnx.commit()

if __name__ == "__main__":
    from Card import Card
    db = Database()
    print(db.getLastEventDate())


try:
    from src.Card import Card
    from src.Event import Event
    from src.CardOccurance import CardOccurance
except ModuleNotFoundError as err:
    from Card import Card
    from Event import Event
    from CardOccurance import CardOccurance
