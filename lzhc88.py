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
num_pages=[]
num_articles=[]
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
'''
link_list = []
p=1
while(len(link_list)<100):
    try:
        r = requests.get(url, stream=True, params={'q': 'Advanced Persistent Threat', 'page': p})
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        #print('Success!')
        #print(r.url)
        txt = r.text
        soup = BeautifulSoup(txt, features='lxml')
        headlines = soup.find_all('a', class_=re.compile("PromoLink"))#, string=[re.compile(k, re.IGNORECASE) for k in key.split()])
        print(len(headlines))
        if not headlines:
            break
        for headline in headlines:
            link = headline['href']
            if 'programmes' in link and 'news' not in link:
                continue
            else:
                print(link)
                link_list.append(link)
        p+=1
'''
keywords = ['targeted threat','Advanced Persistent Threat',
'phishing','DoS attack','malware','computer virus','spyware',
'malicious bot','ransomware','encryption']
for key in keywords:
    link_list = []
    p=1
    while(len(link_list)<100):
        try:
            r = requests.get(url, stream=True, params={'q': key, 'page': p})
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        else:
            #print('Success!')
            #print(r.url)
            txt = r.text
            soup = BeautifulSoup(txt, features='lxml')
            headlines = soup.find_all('a', class_=re.compile("PromoLink"))#, string=[re.compile(k, re.IGNORECASE) for k in key.split()])
            if not headlines:
                break
            for headline in headlines:
                link = headline['href']
                if 'programmes' in link and 'news' not in link:
                    continue
                else:
                    #print(link)
                    link_list.append(link)
            p+=1
    #print(p)
    #print()
    num_pages.append(p)
    num_articles.append(len(link_list))
    link_dict[key] = link_list.copy()
for element in link_dict:
    if len(element)>=100:
        element = element[:100]

for element in link_dict:
    print(len(element))
print(num_pages)
print(num_articles)
for link in link_dict['Advanced Persistent Threat']:
    print(link)
#print(link_dict['Advanced Persistent Threat'])
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
            





## Problem 2
#Use BeautifulSoup to collect and process the articles contents. Save each article content to a file.

## Problem 3

## Problem 4


