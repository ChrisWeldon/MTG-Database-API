import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src.Database import Database
from src.Card import Card
from src.DataCollector import DataCollector
from src.Inventory import Inventory

#This script needs some work.
#Run when you need occurance data on particular a large set of tournaments collected at once



if __name__ == "__main__":

    #This is a throw away script intended purely for occurence debugging.
    dc = DataCollector()
    tourns = dc.downloadTournamentDates(from_date=('10','24', '2019'), to_date=('10','30', '2019'))
    dc.recordOccData(tourns)
