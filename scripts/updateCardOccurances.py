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
    if(not db.getLastEventDate()):
        dates_tocheck = daterange(date(2018, 10, 4), date.today())
    else:
        dates_tocheck = daterange(db.getLastEventDate(), date.today())
    # Oldest set release date 10/05/2018

    del db
    events = []
    print("GETTING TOURNAMENTS")
    while len(dates_tocheck) > 0:
        print(dates_tocheck[0])
        try:
            concat(events, getEventsDay(date = dates_tocheck[0]))
        except (ServerError, ThrottleError) as err:
            print(err)
            throttleWait()
        else:
            dates_tocheck.pop(0)


    print("GETTING EVENT DATA")
    db = Database()
    while len(events)>0:
        occurances = []
        event = events[0]
        print(event)

        if(event.decks==None):
            try:
                decks = getEventData(event)
            except ThrottleError as err:
                print(err)
                throttleWait()
                continue
            except ServerError as err:
                print(err, " : ", events.pop(0))
                continue
            else:
                event.decks = decks;

        try:
            occ = getOccDataByEvent(event)
        except(ThrottleError, ServerError) as err:
            print(err,   ": When Collecting Occ Data for ", event)
            throttleWait()
            continue

        for title in occ.keys():

            card = db.getCardByTitle(title, date=event.date)

            if card!=False:
                # TODO: Error handle this scraping on echomgt
                # FIXME: Making a lot of redundant calls to EchoMTG
                card.price = getPaperPriceByCard(card)
                #card.tix = getMTGOPriceByCard(card)

                try:
                    occurances.append(CardOccurance(card, event, occ[title],date=event.getDate()));
                except Exception as e:
                    print(card)
                    raise Exception(e)

        for c in occurances:
            db.addCardOccurance(c)
        db.addEvent(events[0])
        del events[0]
