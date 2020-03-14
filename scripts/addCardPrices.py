import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from src import *
from datetime import date, timedelta
import time
import requests, json, time
from urllib.request import Request, urlopen
from requests.exceptions import SSLError, ProxyError

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


headers = requests.utils.default_headers()
headers.update({'User-Agent':UserAgent().random})
proxies = {
    'http':"34.83.71.102:8080",
    'https':"34.83.71.102:8080"
}


class ProxyRotation:
    def __init__(self):
        self.refreshHeaders()
        self.refreshProxyList()
        self.proxy = self.proxies[0]

    def refreshProxyList(self):
        proxies_req = Request('https://www.sslproxies.org/')
        proxies_req.add_header('User-Agent', UserAgent().random)
        proxies_doc = urlopen(proxies_req).read().decode('utf8')

        soup = BeautifulSoup(proxies_doc, 'html.parser')
        proxies_table = soup.find(id='proxylisttable')

        # Save proxies in the array
        proxies = []
        for row in proxies_table.tbody.find_all('tr'):
            proxies.append({
                'http': row.find_all('td')[0].string +":"+row.find_all('td')[1].string,
                'https':row.find_all('td')[0].string +":"+row.find_all('td')[1].string
            })

        self.proxies = proxies
        return proxies

    def refreshHeaders(self):
        headers = requests.utils.default_headers()
        headers.update({'User-Agent':UserAgent().random})
        self.headers = headers
        return headers

    def nextProxy(self):
        del self.proxies[0]
        self.proxy = self.proxies[0]
        return self.proxies[0]

if __name__ == "__main__":
    db = Database()
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
