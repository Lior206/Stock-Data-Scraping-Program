import requests
from bs4 import BeautifulSoup
from random import choice
import html5lib

def writeProxyToFile(proxy):
    try:
        stringTowrite = list(proxy)[0] + ":" + proxy[list(proxy)[0]]
        with open(f"proxyFile.txt", 'a') as f:
            f.write(f'{stringTowrite}\n')
    except Exception as inst:
        with open(f"logging/ErrorsSummary.txt", 'a') as f:
            f.write(f'\nError: at writeProxyToFile:' + inst.__str__())
        print("Error: can't crawl page")

def getProxy():
    url = "https://www.sslproxies.org/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    return {'https' : choice(list(map(lambda x:x[0]+':'+x[1], list(zip(map(lambda x:x.text,
              soup.findAll('td')[::8]),map(lambda x:x.text, soup.findAll('td')[1::8]))))))}


def CollectGoodProxy(req_type, url, **kwargs):
    while True:
        try:
            proxy = getProxy()
            print(proxy)
            r = requests.request(req_type, url, proxies=proxy, timeout=5, **kwargs)
            if r.status_code == 200:
                print("Found Good Proxy! :)")
                writeProxyToFile(proxy)
        except:
            print("Shit Proxy :(")
            pass

CollectGoodProxy('get', "https://finance.yahoo.com/quote/AAPL/")
