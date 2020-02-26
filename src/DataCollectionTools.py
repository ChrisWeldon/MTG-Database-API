import sys, os
import requests, json, time
from bs4 import BeautifulSoup,  NavigableString, Tag
import datetime
import pandas as pd
import numpy as np
import json, csv
from datetime import date
import time

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

# @param from_date: tuple of (month, day, year)
# @param to_date: tuple of (month, day, year)
# @return dictionary of {tournament urls : date}
# collects the tournaments and writes them to a file as well as returning them.
def getEventsRange(from_date = ('10', '16', '2019'), to_date = ('10', '24', '2019'), success = lambda msg : print(msg), fail = lambda msg: print(msg)):
    url = 'https://www.mtggoldfish.com/deck_searches/create?utf8=✓&deck_search%5Bname%5D=&deck_search%5Bformat%5D=standard&deck_search%5Btypes%5D%5B%5D=&deck_search%5Btypes%5D%5B%5D=tournament&deck_search%5Bplayer%5D=&deck_search%5Bdate_range%5D='+str(from_date[0])+'%2F'+str(from_date[1])+'%2F'+str(from_date[2])+'+-+'+str(to_date[0])+'%2F'+str(to_date[1])+'%2F'+str(to_date[2])+'&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Btype%5D=maindeck&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Btype%5D=maindeck&counter=2&commit=Search'

    print(url)

    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    page=requests.get(url,headers=headers)
    soup=BeautifulSoup(page.content,'html.parser')
    total_pages = int(soup.find('div', class_='pagination').findAll('a')[-2].text)
    tourns = {}
    page_num = 1
    while page_num != total_pages:

        print('scraping page: ', page_num)
        table = soup.find('table', class_='table table-responsive table-striped')
        if table == None:
            print('page didnt recieve')
            page=requests.get(url,headers=headers)
            soup=BeautifulSoup(page.content,'html.parser')
            continue
        for row in table.findAll('tr'):
            try:
                id = row.findAll('td')[2].find('a')['href']
                if id not in tourns.keys():
                    tourns[id] = row.findAll('td')[0].text
                    print(tourns[id])
            except IndexError:
                continue

        url = 'https://www.mtggoldfish.com' + soup.find('a', class_='next_page')['href']
        page=requests.get(url,headers=headers)
        soup=BeautifulSoup(page.content,'html.parser')
        page_num = page_num + 1

    return [Event(key, date=tourns[key]) for key in tourns.keys()]


def getEventsDay(date = date.today()):
    url = 'https://www.mtggoldfish.com/deck_searches/create?utf8=✓&deck_search%5Bname%5D=&deck_search%5Bformat%5D=standard&deck_search%5Btypes%5D%5B%5D=&deck_search%5Btypes%5D%5B%5D=tournament&deck_search%5Bplayer%5D=&deck_search%5Bdate_range%5D='+str(date.strftime('%m'))+'%2F'+str(date.strftime('%d'))+'%2F'+str(date.strftime('%Y'))+'+-+'+str(date.strftime('%m'))+'%2F'+str(date.strftime('%d'))+'%2F'+str(date.strftime('%Y'))+'&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B0%5D%5Btype%5D=maindeck&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bcard%5D=&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Bquantity%5D=1&deck_search%5Bdeck_search_card_filters_attributes%5D%5B1%5D%5Btype%5D=maindeck&counter=2&commit=Search'


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

    return [Event(key, date=tourns[key]) for key in tourns.keys()]

# @param card - must be of type Card.
# @return bool - True if successful, False if not
# @description - Scrapes pricing data for echo_id and formats correctly. calls Card.setPrice() with scraped data.
# return probably needs to be more usable.
def getHistoricPricesByCard(card, foil=False, cutoff_date=None):
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
    df.set_index('datetime')
    try:
        card.setPrice(df)
        return True
    except Exception as err:
        print(e)
        return False

# @param event - is object of type Event
# @return - dict of cards with occurance data, False if failed,
def getOccDataByEvent(event):
    if not isinstance(event, Event):
        return False
    if(event.isEmpty()):
        print("Warning: Event is empty" )
    headers = requests.utils.default_headers()
    headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})

    cards = {}
    # get occurance data per deck in event
    for id in event.getDecks():
        url='https://www.mtggoldfish.com/deck/'+id+'#paper'
        page=requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')

        if(page.status_code == 500):
            raise ServerError(page.status_code, "Server Error")

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
    url='https://www.mtggoldfish.com' + event.getEventURL()
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


try:
    from src.Card import Card
    from src.Event import Event
    from src.Database import Database
    from src.ScraperExceptions import *
except ModuleNotFoundError as err:
    from Card import Card
    from Event import Event
    from Database import Database
    from ScraperExceptions import *

if __name__ == "__main__":
    print("DataCollectionTools.py main called")
    db = Database()

    ## Add QA Testing here
