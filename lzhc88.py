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
                    #        if check_if_word_in_article(link,word) ==True:
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
'''
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
#If other keyword is mentioned in article of one key, then increase distance by 1
#In the case of perfect matching, the other keyword is found in all 100 articles of one key
#Then distance=100
#
#Later divide distance in correlation matrix by number of articles found.
#e.g. if there are 100 articles for keyword i and 5 articles with keyword j in it, then the distance(i,j)=5/100
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
                    if other in f.read():
                        #print(other+" in txt")
                        corr_matrix[i][j]+=1
print(corr_matrix)
corr_matrix_original = copy.deepcopy(corr_matrix)
for i in range(len(corr_matrix)):
    for j in range(len(corr_matrix)):
        if i==j:
            corr_matrix[i][j]=1
        else:
            if corr_matrix[i][j]!=0:
                corr_matrix[i][j]=corr_matrix[i][j]/num_articles[i]
#print(num_articles)
#print(corr_matrix)

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
def cosine_similarity(x,y):#x,y lists
    xy=0
    x_norm=0
    y_norm=0
    for i in range(len(x)):
        xy += x[i]*y[i]
        x_norm+=x[i]**2
        y_norm+=y[i]**2
    sim_xy = xy/(x_norm*y_norm)
    return sim_xy
#####################################################################################
#Calculate correlation between the appearance of each word in article of each key
art_word_corr=[[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
for i in range(len(corr_matrix)):
    x = corr_matrix_original[i]
    #With x as follows, we get the same pearson correlation matrix as in the dataframe
    #x = [corr_matrix[l][i] for l in range(len(corr_matrix))]
    for j in range(len(corr_matrix_original)):
        y=[corr_matrix_original[l][j] for l in range(len(corr_matrix_original))]
        art_word_corr[i][j]=pearson(x,y)
data_art_word_corr = pd.DataFrame({
    #'Keywords':keywords,
    'targeted threat':[art_word_corr[i][0] for i in range(len(art_word_corr))],
    'Advanced Persistent Threat':[art_word_corr[i][1] for i in range(len(art_word_corr))],
    'phishing':[art_word_corr[i][2] for i in range(len(art_word_corr))],
    'DoS attack':[art_word_corr[i][3] for i in range(len(art_word_corr))],
    'malware':[art_word_corr[i][4] for i in range(len(art_word_corr))],
    'computer virus':[art_word_corr[i][5] for i in range(len(art_word_corr))],
    'spyware':[art_word_corr[i][6] for i in range(len(art_word_corr))],
    'malicious bot':[art_word_corr[i][7] for i in range(len(art_word_corr))],
    'ransomware':[art_word_corr[i][8] for i in range(len(art_word_corr))],
    'encryption':[art_word_corr[i][9] for i in range(len(art_word_corr))]
})

############################################################################

data_pearson = pd.DataFrame({
    #'Keywords':keywords,
    'targeted threat':[corr_matrix[i][0] for i in range(len(corr_matrix))],
    'Advanced Persistent Threat':[corr_matrix[i][1] for i in range(len(corr_matrix))],
    'phishing':[corr_matrix[i][2] for i in range(len(corr_matrix))],
    'DoS attack':[corr_matrix[i][3] for i in range(len(corr_matrix))],
    'malware':[corr_matrix[i][4] for i in range(len(corr_matrix))],
    'computer virus':[corr_matrix[i][5] for i in range(len(corr_matrix))],
    'spyware':[corr_matrix[i][6] for i in range(len(corr_matrix))],
    'malicious bot':[corr_matrix[i][7] for i in range(len(corr_matrix))],
    'ransomware':[corr_matrix[i][8] for i in range(len(corr_matrix))],
    'encryption':[corr_matrix[i][9] for i in range(len(corr_matrix))]
})
corr_pearson = data_pearson.corr(method='pearson')

#plt.figure(figsize=(8,8))
fig,axs = plt.subplots(1,2)
sns.heatmap(corr_pearson,cmap='BrBG',annot=True,annot_kws={'size':6},ax=axs[0])
sns.heatmap(data_art_word_corr,cmap='BrBG',annot=True,annot_kws={'size':6},ax=axs[1])
#fig.tight_layout()
plt.suptitle('Pearson Correlation Heat Map', fontsize=15, fontweight='bold')
plt.show()

############################################################################################################
#Work with google searches
#Extract the related searches and look if one of the other keywords
#is in the related searches
url_google = 'https://www.google.com/search'
###############################################################################################################
#Work with wikipedia articles
#Find how often the other key words are mentioned in the wikipedia articles
url_wikipedia = 'https://en.wikipedia.org/wiki/'
corr_matrix_2 = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
i=0
for key in keywords:
    if key=='malicious bot':
        key = 'internet bot'
    j=0
    for other_key in keywords:
        key_in_wikipedia = check_if_word_in_wikipedia_website(url_wikipedia+key,other_key)
        #print(key_in_wikipedia)
        corr_matrix_2[i][j]=key_in_wikipedia
        j+=1
    i+=1
#################################
#Calculate correlation between the number of appearances of each word in wikipedia article of each key
print(corr_matrix_2)

wiki_word_corr=[[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
for i in range(len(corr_matrix_2)):
    x = corr_matrix_2[i]
    for j in range(len(corr_matrix_2)):
        y=[corr_matrix_2[l][j] for l in range(len(corr_matrix_2))]
        wiki_word_corr[i][j]=pearson(x,y)

for i in wiki_word_corr:
    print(i)
data_wiki_word_corr = pd.DataFrame({
    #'Keywords':keywords,
    'targeted threat':[wiki_word_corr[i][0] for i in range(len(wiki_word_corr))],
    'Advanced Persistent Threat':[wiki_word_corr[i][1] for i in range(len(wiki_word_corr))],
    'phishing':[wiki_word_corr[i][2] for i in range(len(wiki_word_corr))],
    'DoS attack':[wiki_word_corr[i][3] for i in range(len(wiki_word_corr))],
    'malware':[wiki_word_corr[i][4] for i in range(len(wiki_word_corr))],
    'computer virus':[wiki_word_corr[i][5] for i in range(len(wiki_word_corr))],
    'spyware':[wiki_word_corr[i][6] for i in range(len(wiki_word_corr))],
    'malicious bot':[wiki_word_corr[i][7] for i in range(len(wiki_word_corr))],
    'ransomware':[wiki_word_corr[i][8] for i in range(len(wiki_word_corr))],
    'encryption':[wiki_word_corr[i][9] for i in range(len(wiki_word_corr))]
})
data_pearson_2 = pd.DataFrame({
    #'Keywords':keywords,
    'targeted threat':[corr_matrix_2[i][0] for i in range(len(corr_matrix_2))],
    'Advanced Persistent Threat':[corr_matrix_2[i][1] for i in range(len(corr_matrix_2))],
    'phishing':[corr_matrix_2[i][2] for i in range(len(corr_matrix_2))],
    'DoS attack':[corr_matrix_2[i][3] for i in range(len(corr_matrix_2))],
    'malware':[corr_matrix_2[i][4] for i in range(len(corr_matrix_2))],
    'computer virus':[corr_matrix_2[i][5] for i in range(len(corr_matrix_2))],
    'spyware':[corr_matrix_2[i][6] for i in range(len(corr_matrix_2))],
    'malicious bot':[corr_matrix_2[i][7] for i in range(len(corr_matrix_2))],
    'ransomware':[corr_matrix_2[i][8] for i in range(len(corr_matrix_2))],
    'encryption':[corr_matrix_2[i][9] for i in range(len(corr_matrix_2))]
})
#print(data_pearson_2)
corr_pearson_2 = data_pearson_2.corr(method='pearson')  
#print(corr_pearson)
#print(corr_pearson_2)
#############################################################
#plt.figure(figsize=(8,8))

fig,axs = plt.subplots(1,2)
sns.heatmap(corr_pearson_2,cmap='BrBG',annot=True,annot_kws={'size':6},ax=axs[0])
sns.heatmap(data_wiki_word_corr,cmap='BrBG',annot=True,annot_kws={'size':6},ax=axs[1])
#fig.tight_layout()
plt.show()
fig,axs = plt.subplots(1,2)
sns.heatmap(corr_pearson_2,cmap='BrBG',annot=True,annot_kws={'size':6},ax=axs[0])
sns.heatmap(corr_pearson,cmap='BrBG',annot=True,annot_kws={'size':6},ax=axs[1])
#fig.tight_layout()
plt.show()
###########################################################################
#Make second correlation matrix such that all values are between 0 and 1
#divide by the number of times the word of wiki article appears
for i in range(len(corr_matrix_2)):
    for j in range(len(corr_matrix_2)):
        if corr_matrix_2[i][j]!=0:
            corr_matrix_2[i][j]=corr_matrix_2[i][j]/corr_matrix_2[i][i]

print(corr_matrix_2)
##mean between corr_matrix and corr_matrix_2
dist_matrix = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
for i in range(len(corr_matrix_2)):
    for j in range(len(corr_matrix_2)):
        dist_matrix[i][j]=(corr_matrix[i][j]+corr_matrix_2[i][j])
        if dist_matrix[i][j]!=0:
            dist_matrix[i][j]/=2
print(dist_matrix)
data_pearson_mean = pd.DataFrame({
    #'Keywords':keywords,
    'targeted threat':[dist_matrix[i][0] for i in range(len(dist_matrix))],
    'Advanced Persistent Threat':[dist_matrix[i][1] for i in range(len(dist_matrix))],
    'phishing':[dist_matrix[i][2] for i in range(len(dist_matrix))],
    'DoS attack':[dist_matrix[i][3] for i in range(len(dist_matrix))],
    'malware':[dist_matrix[i][4] for i in range(len(dist_matrix))],
    'computer virus':[dist_matrix[i][5] for i in range(len(dist_matrix))],
    'spyware':[dist_matrix[i][6] for i in range(len(dist_matrix))],
    'malicious bot':[dist_matrix[i][7] for i in range(len(dist_matrix))],
    'ransomware':[dist_matrix[i][8] for i in range(len(dist_matrix))],
    'encryption':[dist_matrix[i][9] for i in range(len(dist_matrix))]
})
corr_pearson_mean = data_pearson_mean.corr(method='pearson') 
fig,axs = plt.subplots(1,2)
sns.heatmap(corr_pearson_mean,cmap='BrBG',annot=True,annot_kws={'size':6},ax=axs[0])
sns.heatmap(corr_pearson,cmap='BrBG',annot=True,annot_kws={'size':6},ax=axs[1])
#fig.tight_layout()
plt.show()
##Define distance as:
#If dist_matrix[i][j]!=0 then distance between word i and j is first order, directly connected
#If not then create matrix where matrix[i][j]=1-dist_matrix[i][j]
#Now run a path finding algorithm to find the shortest path between all words i, j that are not di


###########################################################################
##Calculate distance##
class Node:
    def __init__(self,ID,state,action,path_cost):
        self.ID=ID
        self.state=state
        self.action = action
        self.path_cost = path_cost

class State:
    def __init__(self,partial_tour):
        self.partial_tour=partial_tour
    
    def get(self):
        return self.partial_tour  
def basic_greedy():
    node = Node(0,State([0]),0,0)
    path = [node.ID]
    while len(path)!=num_cities:
        successors = []
        for i in range(1,num_cities):#all successors
            if i==node.ID:
                continue
            if i in path:
                continue
            new_id = i
            new_partial_tour=node.state.get().copy()
            new_partial_tour.append(i)
            new_state = State(new_partial_tour)
            new_dist = dist_matrix[node.ID][i]
            new_pathcost = node.path_cost+new_dist
            new_node = Node(new_id,new_state,new_dist,new_pathcost)
            successors.append(new_node)
        node = min(successors,key=lambda node:node.action)
        path.append(node.ID)
    path_cost=node.path_cost+(dist_matrix[0][node.ID])
    return path,path_cost


'''
##Save results of algorithm in distance.xlsx 
# First make my matrix into a dictionary
# Then convert python dictionary into pandas dataframe
#
writer = pd.ExcelWriter('./distance1.xlsx',engine='xlsxwriter')
data1 = pd.DataFrame({
    'Keywords':keywords,
    'targeted threat':[cosine_sim_correlation[i][0] for i in range(len(cosine_sim_correlation))],
    'Advanced Persistent Threat':[cosine_sim_correlation[i][1] for i in range(len(cosine_sim_correlation))],
    'phishing':[cosine_sim_correlation[i][2] for i in range(len(cosine_sim_correlation))],
    'DoS attack':[cosine_sim_correlation[i][3] for i in range(len(cosine_sim_correlation))],
    'malware':[cosine_sim_correlation[i][4] for i in range(len(cosine_sim_correlation))],
    'computer virus':[cosine_sim_correlation[i][5] for i in range(len(cosine_sim_correlation))],
    'spyware':[cosine_sim_correlation[i][6] for i in range(len(cosine_sim_correlation))],
    'malicious bot':[cosine_sim_correlation[i][7] for i in range(len(cosine_sim_correlation))],
    'ransomware':[cosine_sim_correlation[i][8] for i in range(len(cosine_sim_correlation))],
    'encryption':[cosine_sim_correlation[i][9] for i in range(len(cosine_sim_correlation))]
})

data1.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()
writer = pd.ExcelWriter('./distance2.xlsx',engine='xlsxwriter')
data1 = pd.DataFrame({
    'Keywords':keywords,
    'targeted threat':[cosine_sim_correlation_2[i][0] for i in range(len(cosine_sim_correlation_2))],
    'Advanced Persistent Threat':[cosine_sim_correlation_2[i][1] for i in range(len(cosine_sim_correlation_2))],
    'phishing':[cosine_sim_correlation_2[i][2] for i in range(len(cosine_sim_correlation_2))],
    'DoS attack':[cosine_sim_correlation_2[i][3] for i in range(len(cosine_sim_correlation_2))],
    'malware':[cosine_sim_correlation_2[i][4] for i in range(len(cosine_sim_correlation_2))],
    'computer virus':[cosine_sim_correlation_2[i][5] for i in range(len(cosine_sim_correlation_2))],
    'spyware':[cosine_sim_correlation_2[i][6] for i in range(len(cosine_sim_correlation_2))],
    'malicious bot':[cosine_sim_correlation_2[i][7] for i in range(len(cosine_sim_correlation_2))],
    'ransomware':[cosine_sim_correlation_2[i][8] for i in range(len(cosine_sim_correlation_2))],
    'encryption':[cosine_sim_correlation_2[i][9] for i in range(len(cosine_sim_correlation_2))]
})

data1.to_excel(writer, sheet_name='Sheet1', index=False)
writer.save()

## Problem 4
df1 = pd.read_excel('./distance1.xlsx')
df2 = pd.read_excel('./distance2.xlsx')
#sns.pairplot(data=df1,hue='Keywords')
'''