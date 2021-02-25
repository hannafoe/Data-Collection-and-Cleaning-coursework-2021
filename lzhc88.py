import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from lxml import html
import textwrap
import re
##python version 3.8
## Problem 1
#Python program that downloads the webpage content (from BBC news)
#of the top 100 articles relevant to the given keywords from
#the following url: https://www.bbc.co.uk/news
url = 'https://www.bbc.co.uk/search'
link_dict ={}
try:
    res = requests.get(url,stream=True,timeout=0.3)
    # If the response was successful, no Exception will be raised
    res.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
    print(f'Other error occurred: {err}')
else:
    print('Success!')
    

keywords = ['targeted threat','Advanced Persistent Threat',
'phishing','DoS attack','malware','computer virus','spyware',
'malicious bot','ransomware','encryption']
for key in keywords:
    link_list = []
    p=0
    while(len(link_list)<100):

    try:
        res = requests.get(url,stream=True,params={'q':key,'page':p})
        res.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')
        r = requests.get(url,stream=True,params={'q':key,'page':p})
        print(r.url)
        txt = r.text
        soup = BeautifulSoup(txt,features='lxml')
        headlines = soup.find_all('a',class_=re.compile("PromoLink"),string=[re.compile(k,re.IGNORECASE) for k in key.split()])
        for headline in headlines:
            link = headline['href']
            if 'programmes' in link:
                continue
            else:
                print(link)
                print()
        #print(soup.head)
        #print(soup.title)
        #print(soup.body.b)
        #links = soup.select('div div')
        #print(links)
        #<ul role="list" spacing="responsive" class="ssrcss-1a1yp44-Stack e1y4nx260">
        #li
        #links = soup.find_all('a',string=re.compile(key,re.IGNORECASE))
        #stripped = re.sub('<[^<]+?>','',txt)
        #print(stripped)
        #kern = html.fromstring(r.content)
        #for link in kern.xpath("//span[contains(@class,'one-click-content')]"):
        #    if link.text:
        #        l = link.text.strip()
        #        print(textwrap.fill(s))
        #print(kern)
        #print(txt)
        #print(soup.prettify())
        #links = soup.find_all()
        #for link in links:
        #    print(link)
        break





## Problem 2
#Use BeautifulSoup to collect and process the articles contents. Save each article content to a file.

## Problem 3

## Problem 4


