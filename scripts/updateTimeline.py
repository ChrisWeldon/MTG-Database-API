import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src.Database import Database
from src.Event import Event
from src.Card import Card
from src.DataCollectionTools import *
from datetime import date

db = Database()
today = date.today()
events = []

# Oldest set release date 10/05/2018
if(not db.getLastEventDate()):
    events = getEvents(from_date=('10','1', '2019'), to_date=(today.strftime('%m'),today.strftime('%d'),today.strftime('%Y')))
