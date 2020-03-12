#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src import *
from datetime import date, timedelta
import time

def throttleWait(wait=30):
    print("Throttle Wait")
    time.sleep(wait)

def daterange(first, last):
    dates = []
    for n in range(int ((last - first).days)+1):
        dates.append(first + timedelta(n))
    return dates

def concat(list1, list2):
    for e in list2:
        if e not in list1:
            list1.append(e)

if __name__ == "__main__":
    db = Database()
    cards = db.getCards()


    for card in cards:
        print(card)
        if db.getCardPriceByDate(card, date(2020,3,10)) != None:
            continue
        if db.getCardPriceByDate(card, card.rotation_date) != None:
            continue
        card.tix = getMTGOPriceByCard(card)
        card.price = getPaperPriceByCard(card)

        prices= card.CardPrices()
        db.addCardPrices(prices)
