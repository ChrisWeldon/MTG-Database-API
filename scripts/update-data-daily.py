## This is a main process

## Collects all cards in mtg-time-series.cards and gathers all respective timelines and uploads them to database
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src.Database import Database
from src.Card import Card
from src.DataCollector import DataCollector
from src.Inventory import Inventory
import pandas as pd
from datetime import date

def update_timeline():

    db = Database()
    dc = DataCollector()

    last_day = db.getLastCollectedDate() # Get the day to begin the data collection from
    today = date.today() # Get the day to end the data collection, current day
    print("Starting data collection for from day ", last_day , " to ",today )
    try:
        #Get the tournaments and save them as well as write them to a file
        # tourns = dc.downloadTournamentDates(from_date=(last_day.strftime('%m'),last_day.strftime('%d'), last_day.strftime('%Y')),
        #                                         to_date=(today.strftime('%m'),today.strftime('%d'), today.strftime('%Y')))


        tourns = dc.downloadTournamentDates(from_date=('10','30', '2019'),
                                                to_date=(today.strftime('%m'),today.strftime('%d'), today.strftime('%Y')))
    except AttributeError as e:
        # This happens if there are no new tournaments left
        print(e)
        print('No tournaments to collect data from')
        return

    print(tourns)
    for url in tourns:
        db.addTournament(url, tourns[url]) # Add each new tournament to the database

    # Refactor this below code
    dc.recordOccData(tourns) # collect the Occurance data and write it to a file to be opened later. This is a shitty way of doing it

    # Create new inventory with all the cards in the database, called global_invent
    global_inventory = Inventory(cards = db.getCardsInCollection())

    # This functionality should be baked into Inventory
    # Loop through each card and apply the pricing data
    for card in global_inventory.getCards():
        try:
            print(str(card) + ": Downloading price data")
            dc.get_historical_prices_by_card(card) #Collect Data and get prices
        except Exception as e:
            print(e)

    # This functionality should be baked into Inventory
    # Loop through each card and trim pricing data. The trim is so that there is not a mass upload of already uploaded data
    for card in global_inventory.getCards():
        card.price = card.price[card.price['datetime']>=pd.to_datetime(last_day.strftime('%Y-%m-%d'))]

    # This functionality should be baked into Inventory
    # Loop through cards in inventory and put in the Occurance data then compile it, then upload the timeline to the database
    for card in global_inventory.getCards():
        card.loadOccFromFile(file="/Users/chrisevans/Projects/MTG_Database/data/occurance_data"+today.strftime("%b-%d-%Y")+".csv")
        card.assembleTimeline()
        print(str(card))


        try:
            db.uploadCardTimeline(card)
        except Exception as e: # should be some sql error, make more specific when you figure it out uploads
            print(e)
            continue


if __name__=="__main__":
    # This is a base script to be run on systemd service daily
    update_timeline()
