import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src.Database import Database
from src.Event import Event
from src.Card import Card
from src.DataCollectionTools import *

# Current Sets in standard
ELD = getCardsBySet(set_url="/set/ELD/throne-of-eldraine/")
CORE = getCardsBySet(set_url="/set/M20/core-set-2020/")
WAR = getCardsBySet(set_url="/set/WAR/war-of-the-spark/")
RNA = getCardsBySet(set_url="/set/RNA/ravnica-allegiance/")
GRN = getCardsBySet(set_url="/set/GRN/guilds-of-ravnica/")

db = Database()
db.addCards(ELD)
db.addCards(CORE)
db.addCards(WAR)
db.addCards(RNA)
db.addCards(GRN)
