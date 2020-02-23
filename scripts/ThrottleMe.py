# A script with the sole purpose of getting me throttled on MTGGoldfish

import sys, os
import requests, json, time
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup,  NavigableString, Tag
from fake_useragent import UserAgent
import random


ua = UserAgent() # From here we generate a random user agent
proxies = [] # Will contain proxies [ip, port]

# Main function
def main():
  # Retrieve latest proxies
  proxies_req = Request('https://www.sslproxies.org/')
  proxies_req.add_header('User-Agent', ua.random)
  proxies_doc = urlopen(proxies_req).read().decode('utf8')

  soup = BeautifulSoup(proxies_doc, 'html.parser')
  proxies_table = soup.find(id='proxylisttable')

  # Save proxies in the array
  for row in proxies_table.tbody.find_all('tr'):
    proxies.append({
      'ip':   row.find_all('td')[0].string,
      'port': row.find_all('td')[1].string
    })

  # Choose a random proxy
  proxy_index = random_proxy()
  proxy = proxies[proxy_index]

  for n in range(1, 100):
    req = Request('http://icanhazip.com')
    req.set_proxy(proxy['ip'] + ':' + proxy['port'], 'http')

    # Every 10 requests, generate a new proxy
    if n % 10 == 0:
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

    # Make the call
    try:
      my_ip = urlopen(req).read().decode('utf8')
      print('#' + str(n) + ': ' + my_ip)
    except: # If error, delete this proxy and find another one
      del proxies[proxy_index]
      print('Proxy ' + proxy['ip'] + ':' + proxy['port'] + ' deleted.')
      proxy_index = random_proxy()
      proxy = proxies[proxy_index]

# Retrieve a random index proxy (we need the index to delete it if not working)
def random_proxy():
  return random.randint(0, len(proxies) - 1)


def throttle():
    while True:
        headers = requests.utils.default_headers()
        headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})

        url='https://www.mtggoldfish.com'
        page=requests.get(url,headers=headers)
        url='https://www.mtggoldfish.com/metagame/standard#paper'
        page=requests.get(url,headers=headers)
        url='https://www.mtggoldfish.com/prices/paper/standard'
        page=requests.get(url,headers=headers)

        soup=BeautifulSoup(page.content,'html.parser')

        if(str(soup)==str('Throttled\n')):
            print("Throttled")
            break


if __name__ == "__main__":
    main()
