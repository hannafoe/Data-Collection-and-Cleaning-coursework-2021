import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
from lxml import html
import textwrap
import re
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import xlsxwriter
from statistics import mean
import copy
##python version 3.8
#reusable functions and variables
keywords = ['targeted threat','Advanced Persistent Threat',
'phishing','DoS attack','malware','computer virus','spyware',
'malicious bot','ransomware','encryption']

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

def check_if_word_in_article(url,word):
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
def check_if_word_in_wikipedia_website(url,word):
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
        count = soup.get_text().count(word)
        '''
        if len(word.split())>1:
            #print(word.split())
            for split_word in word.split():
                partly_similar= soup.get_text().count(split_word)
                partly_similar/=4
                count+=partly_similar'''
        return count
        #if word in soup.get_text():
        #    count+=1
            
        

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
                #print(headline)
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
                    #        if check_if_word_in_article(link,word) ==True:
                    #            relevant_url=True
                    #            break
                    relevant_url=True
                    if good_url==True and relevant_url==True:
                        #print(link)
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

## Problem 3#########################################################################################################################
#Program to calculate the semantic distances between each two keywords
#which belong to the list of keywords saved in keywords.xlsx
#First use data downloaded from BBC news
#
##Repeated code in case part 1 and 2 are commented out
num_articles=[0,0,0,0,0,0,0,0,0,0]
cur_dir = os.path.dirname(os.path.abspath(__file__))
new_dir = "articles"
path = os.path.join(cur_dir,new_dir)
#
#FIRST METHOD TO FIND THE SIMILARITY BETWEEN WORDS##
#Search for the other keywords in the articles
#If keyword i is mentioned in article of key j, then increase occur_matrix[i][j] value by 1
#In the case that a keyword i is very very similar, keyword i is found in all 100 articles of key j
#Then occur_matrix[i][j]=100
#
occur_matrix = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
i=-1
k=0
for key in keywords:
    i+=1
    current = key
    for file in os.listdir(path):
        if file.startswith(key):
            num_articles[i]+=1
            path_file = os.path.join(path,file)
            with open(path_file,'r',encoding='utf8',errors='ignore') as f:
                j=-1
                for other in keywords:
                    j+=1
                    f.seek(0)
                    if other in f.read():
                        occur_matrix[i][j]+=1
#Now we have the occurrence matrix
print(occur_matrix)
#Save this original occurrence matrix
occur_matrix_original = copy.deepcopy(occur_matrix)
######################################################################################
#NOT USED#
#Now create a new version, which divides every value occur_matrix[i][j]
#by the number of articles found for key i
#and gives occur_matrix[i][j]=1 if i==j
#for i in range(len(occur_matrix)):
#    for j in range(len(occur_matrix)):
#        if i==j:
#            occur_matrix[i][j]=1
#        else:
#            if occur_matrix[i][j]!=0:
#                occur_matrix[i][j]=occur_matrix[i][j]/num_articles[i]
########################################################################################
#FUNCTIONS TO CALCULATE THE SIMILARITY BETWEEN TWO KEYWORDS#############################
#Function to calculate the pearson correlation between two keywords i and j
#Did not use this in the end because of the negative correlation
#NOT USED#
def pearson(x,y):#x,y lists
    cov=0
    std_x=0
    std_y=0
    x_mean = mean(x)
    y_mean = mean(y)
    for i in range(len(x)):
        cov += (x[i]-x_mean)*(y[i]-y_mean)
        std_x +=(x[i]-x_mean)**2
        std_y += (y[i]-y_mean)**2
    if ((std_x*std_y)**0.5)==0:
        pearson_xy = 0
    else:
        pearson_xy = cov/((std_x*std_y)**0.5)
    return pearson_xy

#Instead used cosine_similarity as measure of similarity between two keywords
#USED#
def cosine_similarity(x,y):#x,y lists
    xy=0
    x_norm=0
    y_norm=0
    for i in range(len(x)):
        xy += x[i]*y[i]
        x_norm+=x[i]**2
        y_norm+=y[i]**2
    
    if ((x_norm**0.5)*(y_norm**0.5))==0:
        sim_xy = 0
    else:
        sim_xy = xy/((x_norm**0.5)*(y_norm**0.5))
    return sim_xy

def create_dataframe(matrix):
    df = pd.DataFrame({
        'targeted threat':[matrix[i][0] for i in range(len(matrix))],
        'Advanced Persistent Threat':[matrix[i][1] for i in range(len(matrix))],
        'phishing':[matrix[i][2] for i in range(len(matrix))],
        'DoS attack':[matrix[i][3] for i in range(len(matrix))],
        'malware':[matrix[i][4] for i in range(len(matrix))],
        'computer virus':[matrix[i][5] for i in range(len(matrix))],
        'spyware':[matrix[i][6] for i in range(len(matrix))],
        'malicious bot':[matrix[i][7] for i in range(len(matrix))],
        'ransomware':[matrix[i][8] for i in range(len(matrix))],
        'encryption':[matrix[i][9] for i in range(len(matrix))]
    })
    df.rename(index={0:'targeted threat',1:'Advanced Persistent Threat',2:'phishing',3:'DoS attack',
            4:'malware',5:'computer virus',6:'spyware',7:'malicious bot',8:'ransomware',9:'encryption'
            },inplace=True)
    return df
def plot_heatmap(df,title):
    fig, ax = plt.subplots()
    ax = sns.heatmap(df,cmap='BrBG',annot=True,annot_kws={'size':6})
    ax.set_title(title, fontsize=10, fontweight='bold')
    fig.tight_layout()
    plt.show()
def calculate_cosine_similarity(matrix,new_matrix):
    for i in range(len(matrix)):
        x = matrix[i]
        for j in range(len(matrix)):
            y=[matrix[l][j] for l in range(len(matrix))]
            new_matrix[i][j]=cosine_similarity(x,y)
    return new_matrix
#####################################################################################
#OPTIONAL: JUST FOR COMPARISON WITH THE FINAL SIMILARITY MATRIX#
#Calculate correlation between the appearance of each keyword i in article of keyword j
art_word_corr=[[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
art_word_corr=calculate_cosine_similarity(occur_matrix_original,art_word_corr)
data_art_word_corr=create_dataframe(art_word_corr)
#Optionally print and plot the data#
print(data_art_word_corr)
plot_heatmap(data_art_word_corr,'Correlation article and keywords')
############################################################################################################
#Work with google searches
#Extract the related searches and look if one of the other keywords
#is in the related searches
url_google = 'https://www.google.com/search'

###############################################################################################################
#SECOND METHOD TO FIND THE SIMILARITY BETWEEN WORDS##
##->LATER ADD BOTH TOGETHER##
#Work with wikipedia articles
#Find how often the other key words are mentioned in the wikipedia articles
url_wikipedia = 'https://en.wikipedia.org/wiki/'
occur_matrix_2 = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
i=0
for key in keywords:
    if key=='malicious bot':
        key = 'internet bot'
    j=0
    for other_key in keywords:
        key_in_wikipedia = check_if_word_in_wikipedia_website(url_wikipedia+key,other_key)
        #print(key_in_wikipedia)
        occur_matrix_2[i][j]=key_in_wikipedia
        j+=1
    i+=1
#################################################################################
#OPTIONAL: JUST FOR COMPARISON WITH THE FINAL SIMILARITY MATRIX#
#Calculate correlation between the number of appearances of each word in wikipedia article of each key
wiki_word_corr=[[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
wiki_word_corr = calculate_cosine_similarity(occur_matrix_2,wiki_word_corr)
data_wiki_word_corr = create_dataframe(wiki_word_corr)
#Optionally print and plot the data#
print(data_wiki_word_corr)
plot_heatmap(data_wiki_word_corr,'Correlation wikipedia article and keywords')
###########################################################################
#Make second correlation matrix such that all values are between 0 and 1
#divide by the number of times the word of wiki article appears
#for i in range(len(occur_matrix_2)):
#    for j in range(len(occur_matrix_2)):
#        if occur_matrix_2[i][j]!=0:
#            occur_matrix_2[i][j]=occur_matrix_2[i][j]/occur_matrix_2[i][i]
####################################################################################
##ADD VALUES OF BOTH METHODS TOGETHER TO CALCULATE THE SIMILARITY BETWEEN TWO WORDS##
dist_matrix = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
for i in range(len(occur_matrix_2)):
    for j in range(len(occur_matrix_2)):
        dist_matrix[i][j]=(occur_matrix_original[i][j]+occur_matrix_2[i][j])
print(dist_matrix)
###############################################################################
#OPTIONAL: JUST FOR COMPARISON WITH THE FINAL SIMILARITY MATRIX#
#Calculate cosine similarity###
sources_word_corr=[[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
sources_word_corr = calculate_cosine_similarity(dist_matrix,sources_word_corr)
data_sources_word_corr = create_dataframe(sources_word_corr)
#Optionally print and plot the data#
print(data_sources_word_corr)
plot_heatmap(data_sources_word_corr,'Correlation wiki+articles and keywords')
##########################################################################
##Create a matrix which is symmetric, so that matrix[i][j]==matrix[j][i]
sym_matrix = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
for i in range(len(sym_matrix)):
    for j in range(len(sym_matrix)):
        sym_matrix[i][j]=(dist_matrix[i][j]+dist_matrix[j][i])
print(sym_matrix)
##Calculate the similarity between the words by using cosine similarity##
word_sym_matrix = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
word_sym_matrix = calculate_cosine_similarity(sym_matrix,word_sym_matrix)
data_word_similarities = create_dataframe(word_sym_matrix)
#Optionally print and plot the data#
print(data_word_similarities)
plot_heatmap(data_word_similarities,'Similarity of keywords')
##########################################################################
#FINAL STEP: CALCULATE DISTANCE BETWEEN WORDS
#Since similiarity is scaled such that most similar words have word_sym_matrix[i][j]=1
#And least similar words have word_sym_matrix[i][j]=0
#Define distance(i,j)=1-word_sym_matrix[i][j]
data_word_distances = 1-data_word_similarities
plot_heatmap(data_word_distances,'Distance between words')

##Save data_word_distances in distance.xlsx 
writer = pd.ExcelWriter('./distance.xlsx',engine='xlsxwriter')
data_word_distances.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()

## Problem 4
df = pd.read_excel('./distance.xlsx')
plot_heatmap(data_word_distances,'Distance between words')
#sns.pairplot(data=df1,hue='Keywords')
