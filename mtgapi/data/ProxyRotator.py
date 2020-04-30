from datetime import date, timedelta
import time
import requests, json, time
from urllib.request import Request, urlopen
from requests.exceptions import SSLError, ProxyError
from bs4 import BeautifulSoup,  NavigableString, Tag
from fake_useragent import UserAgent

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
