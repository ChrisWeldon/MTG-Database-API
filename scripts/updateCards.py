import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src.Database import Database
from src.Event import Event
from src.Card import Card
from src.DataCollectionTools import *

# Current Sets in standard
# THB = getCardsBySet(set_url = "/set/THB/theros-beyond-death/")
# ELD = getCardsBySet(set_url="/set/ELD/throne-of-eldraine/")
# CORE = getCardsBySet(set_url="/set/M20/core-set-2020/")
# WAR = getCardsBySet(set_url="/set/WAR/war-of-the-spark/")
# RNA = getCardsBySet(set_url="/set/RNA/ravnica-allegiance/")
# GRN = getCardsBySet(set_url="/set/GRN/guilds-of-ravnica/")

M19 = getCardsBySet(set_url="/set/M19/core-set-2019/")
DOM = getCardsBySet(set_url="/set/DOM/dominaria/")
RIX = getCardsBySet(set_url="/set/RIX/rivals-of-ixalan/")
XLN = getCardsBySet(set_url="/set/XLN/ixalan/")



# FIXME: Add a lot more cards from older sets that were in standard for a while
db = Database()
# db.addCards(THB)
# db.addCards(ELD)
# db.addCards(CORE)
# db.addCards(WAR)
# db.addCards(RNA)
# db.addCards(GRN)

db.addCards(M19)
db.addCards(DOM)
db.addCards(RIX)
db.addCards(XLN)
