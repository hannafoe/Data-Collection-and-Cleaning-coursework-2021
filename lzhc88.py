import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from lxml import html
import textwrap
import re
import os
##python version 3.8
#reusable functions and variables
keywords = ['targeted threat','Advanced Persistent Threat',
'phishing','DoS attack','malware','computer virus','spyware',
'malicious bot','ransomware','encryption']
check_keywords = [['target','threat'],['advance','persist','threat'],
['phish']]
def try_url(url):
    try:
        res = requests.get(url,stream=True,timeout=1)
        # If the response was successful, no Exception will be raised
        res.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return False
    except Exception as err:
        print(f'Other error occurred: {err}')
        return False
    else:
        print("success")
        return True

def check_if_word_in_website(url,word):
    try:
        res = requests.get(url,stream=True)
        res.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        #Get the text component of the website
        txt = res.text
        soup = BeautifulSoup(txt, features='lxml')
        if word in soup.title.get_text():
            return True
        #Extract only the article content
        text_blocks = soup.find_all(attrs={"data-component":"text-block"})
        for text in text_blocks:
            text = text.get_text()
            if word in text:
                return True

def write_urltext_into_file(url,path,i):
    try:
        res = requests.get(url,stream=True)
        res.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        #Get the text component of the website
        txt = res.text
        soup = BeautifulSoup(txt, features='lxml')
        #Extract only the article content
        text_blocks = soup.find_all(attrs={"data-component":"text-block"})
        #Create new text file to store the article
        filename=key+" "+str(i)+".txt"
        path_file = os.path.join(path,filename)
        with open(path_file,'w',encoding='utf8',errors='ignore') as f:
            #Write the title into the text file
            f.write(soup.title.get_text()+"\n")
            #Then write the whole textblock into the file
            for text in text_blocks:
                text = text.get_text()
                f.write(text+"\n")
'''
## Problem 1
#Python program that downloads the webpage content (from BBC news)
#of the top 100 articles relevant to the given keywords from
#the following url: https://www.bbc.co.uk/news
url = 'https://www.bbc.co.uk/search'
link_dict ={}
num_pages=[]
num_articles=[]

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
                print(headline)
                link = headline['href']
                if 'programmes' in link and 'news' not in link:
                    continue
                else:
                    #There are websites with guide in the url that do not open
                    #so check if urls with guide open
                    relevant_url = False
                    good_url = True
                    if 'guides' in link:
                        print(link) 
                        good_url = try_url(link)
                        print(good_url)
                    #Split keyword at space
                    #Check if one of the components of keyword is included in the header
                    #THIS METHOD TAKES AWAY ARTICLES THAT ARE IRRELEVANT; BUT ALSO SOME ARTICLES THAT ARE RELEVANT
                    #SO DECIDED TO TAKE IT OUT
                    #I FIND THE SEARCH ALGORITHM OF BBC MORE ACCURATE
                    #key_split = key.split()
                    #keyInHeader = headline.find_all(string=[re.compile(k, re.IGNORECASE) for k in key_split])
                    #
                    #if none of the keyword's component is in the header, check in the article itself
                    #whether the article contains any of the keyword's components
                    #THIS METHOD TAKES A LONG TIME AND IS NOT THAT HELPFUL: SO DECIDED TO TAKE IT OUT
                    #if not keyInHeader:
                    #    for word in key_split:
                    #        if check_if_word_in_website(link,word) ==True:
                    #            relevant_url=True
                    #            break
                    relevant_url=True
                    if good_url==True and relevant_url==True:
                        print(link)
                        link_list.append(link)
            p+=1
    #print(p)
    #print()
    num_pages.append(p)
    num_articles.append(len(link_list))
    link_dict[key] = link_list.copy()
    #print(len(link_dict[key]))
for element in link_dict:
    if len(link_dict[element])>=100:
        link_dict[element]=link_dict[element][:100]

#print(num_pages)
#print(num_articles)

## Problem 2
#Use BeautifulSoup to collect and process the articles contents. 
# Save each article content to a file.
#
#First create directory in current working directory to store the files
cur_dir = os.path.dirname(os.path.abspath(__file__))
new_dir = "articles"
path = os.path.join(cur_dir,new_dir)

try:
    os.makedirs(path,exist_ok = True)
except OSError as error:
    print("The directory 'articles' could not be created.")

#Now create a text file for each article/url
for key in link_dict:
    i=0
    for url in link_dict[key]:
        i+=1
        write_urltext_into_file(url,path,i)    

## Problem 3
#Program to calculate the semantic distances between each two keywords
#which belong to the list of keywords saved in keywords.xlsx
#First use data downloaded from BBC news
#
#Repeated code in case part 1 and 2 are commented out
num_articles=[0,0,0,0,0,0,0,0,0,0]
cur_dir = os.path.dirname(os.path.abspath(__file__))
new_dir = "articles"
path = os.path.join(cur_dir,new_dir)
#Search for the other keywords in the articles
corr_matrix = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
i=-1
k=0
for key in keywords:
    i+=1
    current = key
    #print(current+"\n")
    for file in os.listdir(path):
        if file.startswith(key):
            num_articles[i]+=1
            path_file = os.path.join(path,file)
            with open(path_file,'r',encoding='utf8',errors='ignore') as f:
                j=-1
                for other in keywords:
                    j+=1
                    f.seek(0)
                    #print(key)
                    if other!=current and other in f.read():
                        #print(other+" in txt")
                        corr_matrix[i][j]+=1
print(corr_matrix)

for i in range(len(corr_matrix)):
    for j in range(len(corr_matrix)):
        if i==j:
            corr_matrix[i][j]=1
        else:
            if corr_matrix[i][j]!=0:
                corr_matrix[i][j]=corr_matrix[i][j]/num_articles[i]
print(num_articles)
print(corr_matrix)
'''
#Work with google searches
#Extract the related searches and look if one of the other keywords
#is in the related searches
url_google = 'https://www.google.com/search'
url_wikipedia = 'https://en.wikipedia.org/wiki/'
for key in keywords:
    try:
        r = requests.get(url_wikipedia+key)
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print(r.url)
        txt = r.text
        soup = BeautifulSoup(txt, features='lxml')
        for other_key in keywords:
            if key == other_key:
                continue
            else:
                key_in_wikipedia = check_if_word_in_website(link,other_key)
                print(key_in_wikipedia)

                
    break        

## Problem 4


