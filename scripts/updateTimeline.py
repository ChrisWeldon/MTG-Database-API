import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from src import *
from datetime import date, timedelta
import time

def throttleWait(wait=10):
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
    if(not db.getLastEventDate()):
        dates_tocheck = daterange(date(2019, 10, 1), date.today())
    else:
        dates_tocheck = daterange(db.getLastEventDate(), date.today())
    # Oldest set release date 10/05/2018

    events = []
    while len(dates_tocheck) > 0:
        print(dates_tocheck[0])
        try:
            concat(events, getEventsDay(date = dates_tocheck[0]))
        except (ServerError, ThrottleError) as err:
            print(err)
            throttleWait()
        else:
            dates_tocheck.pop(0)

    occ_q =[]

    while len(events)>0:
        try:
            decks = getEventData(events[0])
        except ThrottleError as err:
            print(err)
            throttleWait()
        except ServerError as err:
            print(err, " : ", events.pop(0))
        else:
            event = events.pop(0)
            event.setDecks(decks);
            occ_q.append(event)

    db.addEvents(events)

    
