import mysql.connector
import datetime
import sys, json
import numpy as np
import pandas as pd
import math



## Important database notes
# there will be a row per card/day table
# there will be a table of all cards, ids, sets they belong to


#Database interaction Object

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

    def isConnected():
        if(self.cnx != None):
            return True
        else:
            return False

    #param: Card Object with data all data.
    #returns: boolean true if upload successful boolean false if not successful.
    def uploadCardTimeline(self, card):
        # assert isinstance(card, Card), "Expected instance of card, got " + card

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

            try:
                check = ("SELECT * WHERE rowid = " + str(card.echo_id)+"-"+str(row['datetime']))
                cursor.execute(check)

                if cursor.fetchone()[0]:
                    delete = ("DELETE FROM card_series WHERE rowid = " + str(card.echo_id)+"-"+str(row['datetime']))
                    print("EXISTS, DELETING " + str(card.echo_id)+"-"+str(row['datetime']))
                    cursor.execute(delete)
                    self.cnx.commit()

                cursor.execute(insert_timeline, insert_timeline_data)
                self.cnx.commit()
            except Exception as e:
                print(e)
                continue
        sys.stdout.write("]\n")

    def addCardToCollecton(self, card):
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
        id = cursor.lastrowid
        return id

    def addCardsToCollection(self, cards):
        for card in cards:
            self.addCardToCollecton(card)
            print(str(card.echo_id) + " - " + card.title)

    def getCardsInCollection(self):
        cursor = self.cnx.cursor()
        query = ("SELECT * FROM cards")
        cursor.execute(query)
        cards = []
        for row in cursor.fetchall():
            cards.append(Card(title=row[0],set = row[1], echo_id = row[5], rarity=row[4]))
        return cards

    def addTournament(self, url, date):
        cursor = self.cnx.cursor()
        t_id = int(url.split('/')[-1])
        insert_tournament = ("INSERT INTO tournaments"
                            """(date, url, id)"""
                            "VALUES (%s, %s, %s)")
        insert_values = (date, url, t_id)
        try:
            cursor.execute(insert_tournament, insert_values)
            self.cnx.commit()
        except Exception as err:
            print(err)
        return t_id


    def getLastCollectedDate(self):
        cursor = self.cnx.cursor()
        query = ("""SELECT MAX(date) FROM `card_series`;""")
        try:
            cursor.execute(query)
        except Exception as err:
            print(err)
        for row in cursor.fetchall():
            return row[0]



if __name__ == "__main__":
    from Card import Card
    db = Database()
    print(db.getLastCollectedDate())
else:
    from src.Card import Card
