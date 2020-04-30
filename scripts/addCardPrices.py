import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from datetime import date, timedelta
import time
import requests, json, time
from urllib.request import Request, urlopen
from requests.exceptions import SSLError, ProxyError

from mtgapi.common.Card import Card
from mtgapi.common.CardPrice import CardPrice
from mtgapi.common.Event import Event
from mtgapi.common.CardOccurance import CardOccurance
from mtgapi.common.Database import Database
from mtgapi.common.exceptions.ScraperExceptions import ServerError, ThrottleError
from mtgapi.common.exceptions.ScraperExceptions import ForbiddenError

from mtgapi.data.ProxyRotator import ProxyRotation
from mtgapi.data.DataCollectionTools import getMTGOPriceByCard, getPaperPriceByCard

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
    db = Database(path='config.json')
    pr = ProxyRotation()
    cards = db.getCards(from_date=date.today())


    for card in cards:
        print(card)
        if card.rotation_date != None and db.getCardPriceByDate(card, card.rotation_date) != None:
            continue
        elif db.getCardPriceByDate(card, date.today()) != None:
            continue

        start = db.getLastCardPriceByCard(card)
        if start==None:
            start = card.release_date
        end = date.today()

        while True:
            try:
                card.tix = getMTGOPriceByCard(card, proxies=pr.proxy, headers=pr.headers)
                break
            except (ForbiddenError, SSLError, ProxyError) as e:
                print(e)
                pr.nextProxy()
                pr.refreshHeaders()


        card.price = getPaperPriceByCard(card)

        prices= card.CardPrices(start=start, end=end)
        db.addCardPrices(prices)
