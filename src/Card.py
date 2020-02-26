import os, csv, json
import pandas as pd
import numpy as np


#Datatype object to represent a Card,
#Card.timeline contains complete timeline of occurances and price (tournement dates not included)
#Card.occ contains dataframe of occurances
#Card.price contains dataframe of pricing history

class Card:
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

    def __init__(self, id=-1, title="", occ_data_path="",price_data_path="",
                occ = pd.DataFrame(columns=occ_data_columns), price=pd.DataFrame(columns=price_data_columns),
                set=None,echo_id=-1, manifest_path="", rarity=None, timeline=pd.DataFrame()):
        assert isinstance(occ, pd.DataFrame), "non dataframe passed through occ"
        assert isinstance(price, pd.DataFrame), "non dataframe passed through price"
        self.id = id
        self.title = title
        self.occ = occ
        self.price = price
        self.price_data_path = price_data_path
        self.occ_data_path = occ_data_path
        self.manifest_path = manifest_path
        self.set = set
        self.echo_id = echo_id
        self.rarity = rarity
        self.timeline = timeline

        if manifest_path != "":
            self.loadManifestFromFile()

        if occ.empty and occ_data_path != "":  # Allows for Initialization from only paths
            self.loadOccFromFile()

        if price.empty and price_data_path != "": # Allows for Initialization from only paths
            self.loadPriceFromFile()

        if not price.empty and not occ.empty:
            self.assembleTimeline()

    # Equality is based solely off id.
    def __eq__(self, o):
        return isinstance(o, Card) and o.id == self.id

    def __str__(self):
        if self.isEmpty():
            return str(self.echo_id) + "-" + str(self.title) + "-EMPTY"
        else:
            return str(self.echo_id) + "-" + str(self.title)

    def setPrice(self, price):
        assert isinstance(price, pd.DataFrame), "price must be instance of Dataframe"
        self.price = price

    def setOcc(self, occ):
        assert isinstance(occ, pd.DataFrame)
        self.occ = occ

    def isEmpty(self):
        # return self.occ.empty or self.price.empty # Missing either Occurence data or pricing data.
        return self.timeline.empty

    def getID(self):
        return self.echo_id

    # Loads price from data collected file and overwrites price_data with loaded data
    # THIS CAME FROM THE NOTEBOOK
    def loadPriceFromFile(self, file=None):
        if file == None:
            csv_path = os.path.join(self.price_data_path)
        else:
            csv_path = file
        try:
            card = pd.read_csv(csv_path,parse_dates=['datetime'])
            card.loc[:,'date_unix'] = card['date_unix']/1000
            card.loc[:,'datetime'] = pd.to_datetime(card['datetime'])
            card.set_index('datetime')
            card.drop('date_unix', axis=1)
            #card.loc[:,'d_price_dollars'] = card['price_dollars'].diff()
            self.price = card
            return True
        except Exception as e: # TODO manage specific errors
            print(e)
            return False

    # Loads price from occ file
    def loadOccFromFile(self,file=None):
        if file == None:
            csv_path = self.occ_data_path
        else:
            csv_path = file
        occ_df = pd.read_csv(csv_path,parse_dates=True,date_parser=self.dateparse)
        card_occurances = occ_df.loc[occ_df['card']==self.title]
        #card_occurances['datetime'] = card_occurances['date'].map(lambda x : datetime.strptime(x, '%Y-%m-%d'))
        card_occurances.loc[:,'datetime'] = pd.to_datetime(card_occurances['date'])
        card_occurances.set_index('datetime')
        card_occurances.loc[:,'raw_per_decks'] = card_occurances['raw']/card_occurances['deck_nums']
        card_occurances.loc[:,'total_first'] = card_occurances['1st Place']

        card_occurances.loc[:,'scaled_placement'] = .5*(card_occurances['1st Place'] + card_occurances['2nd Place']) + .25*(card_occurances['3rd Place'] + card_occurances['4th Place']) + .13*(card_occurances['5th Place'] + card_occurances['6th Place'] + card_occurances['7th Place'] + card_occurances['8th Place'])


        card_occs_nums_only = card_occurances.drop('event', axis=1).drop('date_unix', axis=1).drop('card', axis=1)
        card_occs_stacked = card_occs_nums_only.groupby('datetime').sum().reset_index()

        #the code below should probably be it's one function.

        card_occs_stacked.loc[:,'raw_rolling'] = card_occs_stacked['raw_per_decks'].rolling(window=14).mean()
        #card_occs_stacked.loc[:,'d_raw_rolling'] = card_occs_stacked['raw_rolling'].diff()
        #card_occs_stacked.loc[:,'d_raw_per_decks'] = card_occs_stacked['raw_per_decks'].diff()
        self.occ = card_occs_stacked

    # Overwrites basic metadata with data from file
    # Useful if loading from saved csv
    def loadManifestFromFile(self):
        try:
            csv_path = self.manifest_path
            data = None
            with open(csv_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                headers = next(reader, None)
                data = [r for r in reader]
            #formated as: data = [[title, echo_id, rarity, echo_id, set]]
            data = data[0]
            self.title = data[0]
            self.echo_id = data[1]
            self.rarity = data[2]
            self.set = data[4]
            return True
        except Exception as e:
            print(e)
            return False


    # Compiles and cleans the occurance data and pricing history into one maintainable table.
    def assembleTimeline(self):
        # TODO USE THE MAX DATE BETWEEN THE TWO TABLES
        # min_date = self.price['datetime'].min() if self.price['datetime'].min() < self.occ['datetime'].min() else self.occ['datetime'].min()
        # max_date = self.price['datetime'].max() if self.price['datetime'].max() > self.occ['datetime'].max() else self.occ['datetime'].max()
        #
        # print(min_date)
        # print(max_date)
        if(self.price.empty):
            return
        full_index = pd.date_range(start=self.price['datetime'].min(), end=self.price['datetime'].max(), freq='1D')
        full = pd.DataFrame(columns=['datetime'])
        full['datetime'] = full_index

        table = pd.merge(full,
                        self.price,
                        on='datetime',
                        how='left')
        table  = pd.merge(table,
                         self.occ[['datetime','raw','deck_nums','1st Place','2nd Place',
                                                         '3rd Place','4th Place','5th Place','6th Place','7th Place','8th Place',
                                                         '9th Place','10th Place','11th Place','12th Place','13th Place','14th Place',
                                                         '15th Place','16th Place','(9-0)','(8-0)','(7-0)','(6-0)','(5-0)','(6-1)',
                                                         '(5-2)','(8-1)','(7-2)','(7-1)','(6-2)']],
                         on='datetime',
                         how='left')
        #table.set_index('datetime', inplace=True)
        self.timeline = table

    def dateparse(time_unix):
        return datetime.utcfromtimestamp(int(time_unix)/1000).strftime('%Y-%m-%d %H:%M:%S')


if __name__ == "__main__":
    print("Card Main Called")
