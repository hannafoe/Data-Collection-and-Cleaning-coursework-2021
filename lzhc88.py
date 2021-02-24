import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
##python version 3.8
## Problem 1
#Python program that downloads the webpage content (from BBC news)
#of the top 100 articles relevant to the given keywords from
#the following url: https://www.bbc.co.uk/news
url = 'https://www.bbc.co.uk/news'
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
    try:
        res = requests.get(url,stream=True,params={'q':key})
        res.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')
        txt = requests.get(url,stream=True,params={'q':key}).text
        soup = 





## Problem 2

## Problem 3

## Problem 4


