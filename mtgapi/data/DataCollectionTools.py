import sys, os
import requests, json, time
from bs4 import BeautifulSoup,  NavigableString, Tag
import datetime
import pandas as pd
import numpy as np
import json, csv
from datetime import date
import time
from fake_useragent import UserAgent
from mtgapi.common.Event import Event
from mtgapi.common.Card import Card
from mtgapi.common.ScraperExceptions import ForbiddenError
from mtgapi.common.ScraperExceptions import ThrottleError

# @param set_url: string representing url of set
# @return array of Card objects: card are effectively empty aside from the manifest data
def getCardsBySet(set_url="/set/THB/theros-beyond-death/", rarities=['rare', 'mythic-rare']):
    url='https://www.echomtg.com' + set_url
    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    page=requests.get(url,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')

    data = []
    for card in soup.find('table', id='set-table').findAll('tr'):
        if card.find('a', class_='list-item'):
            data.append({'title': card.find('a', class_='list-item').text,
                        'url': card.find('a', class_='list-item')['href'],
                        'rarity': card['class'][0],
                        'id': card.find('a', class_='list-item')['href'].split('/')[2],
                        'set': set_url})

    return_cards = []
    for object in data:
        if object['rarity'] in rarities:
            return_cards.append(Card(echo_id=object['id'], title=object['title'], rarity=object['rarity'], set=object['set']))
    return return_cards

def getEventsDayOnePage(date = date.today(), format='standard'):
    #FIXME sometimes there still might be multiple pages!!!

    url = 'https://www.mtggoldfish.com/deck_searches/create?utf8=✓&deck_search%5Bname%5D=&deck_search%5Bformat%5D='+format+'&deck_search%5Btypes%5D%5B%5D=&deck_search%5Btypes%5D%5B%5D=tournament&deck_search%5Bplayer%5D=&deck_search%5Bdate_range%5D='+str(date.strftime('%m'))+'%2F'+str(date.strftime('%d'))+'%2F'+str(date.strftime('%Y'))+'+-+'+str(date.strftime('%m'))+'%2F'+str(date.strftime('%d'))+'%2F'+str(date.strftime('%Y'))+'&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Btype%5D=maindeck&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Btype%5D=maindeck&counter=2&commit=Search'

    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    page=requests.get(url,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')

    if(page.status_code == 500):
        print("Status Code: 500")
        raise ServerError(page.status_code, "Server Error")

    if(str(soup)==str('Throttled\n')):
        print("Throttled")
        raise ThrottleError("Throttled on MTG Goldfish")

    ## Probing for potential bug, will delete later
    try:
        total_pages = int(soup.find('div', class_='pagination').findAll('a')[-2].text)
        print("TOTAL PAGES: ", total_pages)
    except Exception as e:
        #passing silently because this block should be removed after bug discovery
        pass

    tourns = {}
    table = soup.find('table', class_='table table-responsive table-striped')


    if table == None:
        return []
    for row in table.findAll('tr'):
        try:
            id = row.findAll('td')[2].find('a')['href']
            if id not in tourns.keys():
                tourns[id] = row.findAll('td')[0].text
                print(id, " : ", tourns[id])
        except IndexError:
            continue

    return [Event(key, date=tourns[key], format=format) for key in tourns.keys()]

def getEventsDay(date = date.today(), format='standard'):
    #FIXME sometimes there still might be multiple pages!!!

    url = 'https://www.mtggoldfish.com/deck_searches/create?utf8=✓&deck_search%5Bname%5D=&deck_search%5Bformat%5D='+format+'&deck_search%5Btypes%5D%5B%5D=&deck_search%5Btypes%5D%5B%5D=tournament&deck_search%5Bplayer%5D=&deck_search%5Bdate_range%5D='+str(date.strftime('%m'))+'%2F'+str(date.strftime('%d'))+'%2F'+str(date.strftime('%Y'))+'+-+'+str(date.strftime('%m'))+'%2F'+str(date.strftime('%d'))+'%2F'+str(date.strftime('%Y'))+'&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Btype%5D=maindeck&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Btype%5D=maindeck&counter=2&commit=Search'

    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})

    tourns = {}
    while url!=None:

        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')

        if(page.status_code == 500):
            print("Status Code: 500")
            raise ServerError(page.status_code, "Server Error")

        if(str(soup)==str('Throttled\n')):
            print("Throttled")
            raise ThrottleError("Throttled on MTG Goldfish")

        table = soup.find('table', class_='table table-responsive table-striped')
        if table == None:
            break
        for row in table.findAll('tr'):
            try:
                id = row.findAll('td')[2].find('a')['href']
                if id not in tourns.keys():
                    tourns[id] = row.findAll('td')[0].text
                    print(id, " : ", tourns[id])
            except IndexError:
                continue

        next = soup.find('a', class_='next_page')
        if next == None:
            url  = None
        else:
            url = 'https://www.mtggoldfish.com' +next['href']


    return [Event(key, date=tourns[key], format=format) for key in tourns.keys()]

def getPaperPriceByCard(card, foil=False, cutoff_date=None):
    assert isinstance(card, Card)
    if not foil:
        url='https://www.echomtg.com/cache/'+str(card.echo_id)+'.r.json'
    else:
        url='https://www.echomtg.com/cache/'+str(card.echo_id)+'.f.json'
    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    page=requests.get(url,headers=headers)

    price_array = page.json()
    for row in price_array:
        row[0] = datetime.datetime.fromtimestamp(int(row[0])/1000)

    df = pd.DataFrame(columns=['datetime', 'price'], data=np.array(price_array))
    dates = pd.date_range(df['datetime'].min(), date.today())
    dates = dates.to_frame(name='datetime')
    df = df.set_index('datetime')

    df = dates.join(df, on='datetime')
    df = df.set_index('datetime')
    df = df.ffill()
    return df

def getMTGOPriceByCard(card, foil=False, proxies={}, headers= requests.utils.default_headers()):
    assert isinstance(card, Card)
    title = card.title
    formatted_title = title.replace(" // ", " ").replace(" ", "-").replace(",", "").replace("'", "").lower()
    url = 'https://www.goatbots.com/card/ajax_card?search_name=' + formatted_title

    page=requests.get(url, headers = headers, proxies=proxies)
    print(page.status_code)
    if(page.status_code == 403):
        raise ForbiddenError("Goatbots revolked access to pricing history")
    versions = page.json()[1]

    #v[0] is the first entry a card versions pricing array, v[i][0] is the date in str
    version = versions[0]

    for v in versions:
        version_date = datetime.datetime.strptime(v[0][0], "%m/%d/%Y").date()
        if(version_date <= card.release_date):
            version = v
            break

    df = pd.DataFrame(columns=['datetime', 'price'], data=np.array(version))
    df['datetime']  = pd.to_datetime(df['datetime'])

    dates = pd.date_range(df['datetime'].min(), date.today())
    dates = dates.to_frame(name='datetime')
    df = df.set_index('datetime')

    df = dates.join(df, on='datetime')
    df = df.set_index('datetime')
    df = df.ffill()
    return df

def getOccDataByEvent(event, deck_max = 16):
    if not isinstance(event, Event):
        return False
    if(event.isEmpty()):
        print("Warning: Event is empty" )
    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})

    cards = {}
    # get occurance data per deck in event
    decks = event.decks

    if(deck_max != -1):
        decks = decks[:deck_max]
    for id in decks:
        url='https://www.mtggoldfish.com/deck/'+id+'#paper'
        page=requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        try: # No Errors pass Silently PEP 8
            if(page.status_code == 500):
                raise ServerError(page.status_code, "Server Error")
        except ServerError as e:
            print(e)
            continue

        # TODO: Handle Bad Gateway 502
        if(str(soup)==str('Throttled\n')):
            raise ThrottleError("Throttled on MTG Goldfish")

        # deck is private. Not collecting data for private decks
        if 'private' in str(soup.find('div', class_='alert alert-warning')):
            continue


        try:
            table = soup.find('table', class_='deck-view-deck-table')
            description = soup.find('div', class_='deck-view-description')
            place = description.findChildren()[0].nextSibling.strip()[2:]
        except AttributeError as err:
            print(page)
            print(id ," : ", err)
            return False

        for tr in table.findAll('tr'):
            name = tr.find('td', class_='deck-col-card')
            qty = tr.find('td', class_='deck-col-qty')
            if qty:
                name = name.text.strip()
                qty = int(qty.text.strip())
                if name not in cards.keys():
                    cards[name] = {'raw': 0}
                    cards[name]['raw'] =qty #creating quantity for raw occurances
                    cards[name][place] = qty #creating quantity for occurances at that placement
                else:
                    cards[name]['raw'] = cards[name]['raw'] + qty
                    if place not in cards[name].keys():
                        cards[name][place] = qty
                    else:
                        cards[name][place] = cards[name][place] + qty

    return cards

def recordOccData(events):
    with open('/Users/chrisevans/Projects/MTG_Database/data/occurance_data'+date.today().strftime("%b-%d-%Y")+'.csv', 'w', newline='') as csvfile:
        fieldnames = ['card', 'date', 'date_unix', 'raw', 'event', 'deck_nums', '1st Place', '2nd Place', '3rd Place', '4th Place', '5th Place', '6th Place', '7th Place', '8th Place', '9th Place', '10th Place', '11th Place', '12th Place', '13th Place', '14th Place', '15th Place', '16th Place','(9-0)','(8-0)','(7-0)',
        '(6-0)','(5-0)', '(6-1)', '(5-2)','(8-1)','(7-2)','(7-1)','(6-2)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        print(str(len(events)), " events to scrape")
        for event in events.keys():
            print(event)
            event_data = self.downloadEventData(event)
            occ_data = self.downloadOccData(event_data['deck_ids'])
            unix_date = time.mktime(datetime.datetime.strptime(events[event], "%Y-%m-%d").timetuple())
            unix_date = unix_date
            for key in occ_data.keys():
                write_data = {'card':key, 'date': events[event], 'date_unix': unix_date, 'event': event_data['title'], 'deck_nums': len(event_data['deck_ids'])}
                trash_keys = []
                for occ_key in occ_data[key].keys():
                    if occ_key not in fieldnames:
                        trash_keys.append(occ_key)
                for trash_key in trash_keys:
                    occ_data[key].pop(trash_key)
                write_data.update(occ_data[key])
                for field in fieldnames:
                    if field not in write_data.keys():
                        write_data[field] = 0
                writer.writerow(write_data)

def getEventData(event):
    assert isinstance(event, Event)
    url='https://www.mtggoldfish.com' + event.event_url
    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    page=requests.get(url,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')

    if(page.status_code == 500):
        raise ServerError(page.status_code, "Server Error: getEventData")

    if(str(soup)==str('Throttled\n')):
        raise ThrottleError("Throttled on MTG Goldfish")

    # try:
    deck_ids = [deck['data-deckid'] for deck in soup.find('table', class_='table table-condensed table-bordered table-tournament').findAll('tr', class_='tournament-decklist')]
    # except AttributeError as err:
        # return False

    return deck_ids


if __name__ == "__main__":
    print("DataCollectionTools.py main called")
    from CardPrice import CardPrice
    db = Database()
    card = db.getCardByTitle('Teferi, Time Raveler')
    card.tix = getMTGOPriceByCard(card)



    ## Add QA Testing here
