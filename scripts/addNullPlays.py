import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src import *
from datetime import date, timedelta
import time


def daterange(first, last):
    dates = []
    for n in range(int ((last - first).days)+1):
        dates.append(first + timedelta(n))
    return dates

if __name__ == '__main__':
    START_DATE = date(2018, 10, 4)

    db = Database()
    events=db.getEvents();
    cards= db.getCards();
    print(len(cards) , " Total Cards")
    count = 0
    for c in cards:
        count = count+1
        print(c, " : ", count, "/", len(cards))
        if db.allPlaysRecorded(c):
            continue
        c.tix = getMTGOPriceByCard(c)
        c.price = getPaperPriceByCard(c)
        for e in events:
            if e.date < c.release_date:
                continue
            try:
                play = CardOccurance(c,e, {})
            except DatePricingError as e:
                print(e)
                continue
            db.addCardOccurance(play)
