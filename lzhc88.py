import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import xlsxwriter
import seaborn as sns
##python version 3.8
#reusable functions and variables
#first get keywords from excel file

keyword_file = './keywords.xlsx'
try:
    keyword_df = pd.read_excel(pd.ExcelFile(keyword_file))
    keywords = list(keyword_df['Keywords'])
except:
    print('./keywords.xlsx does not exist. Continue with given set of keywords.')
    keywords = ['targeted threat','Advanced Persistent Threat',
    'phishing','DoS attack','malware','computer virus','spyware',
    'malicious bot','ransomware','encryption']


def try_url(url):
    try:
        res = requests.get(url,stream=True,timeout=1)
        # If the response was successful, no Exception will be raised
        res.raise_for_status()
    except HTTPError as http_err:
        #print(f'HTTP error occurred: {http_err}')
        return False
    except Exception as err:
        #print(f'Other error occurred: {err}')
        return False
    else:
        #print("success")
        return True

def check_if_word_in_article(url,word):
    try:
        res = requests.get(url,stream=True)
        res.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return False
    except Exception as err:
        print(f'Other error occurred: {err}')
        return False
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
        return False
    except Exception as err:
        print(f'Other error occurred: {err}')
        return False
    else:
        #Get the text component of the website
        txt = res.text
        soup = BeautifulSoup(txt, features='lxml')
        count = soup.get_text().count(word)
        return count
            
        

def write_urltext_into_file(url,path,i,key):
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
        if not text_blocks:
            print(url)
        #Create new text file to store the article
        filename=key+" "+str(i)+".txt"
        path_file = os.path.join(path,filename)
        with open(path_file,'w',encoding='utf8',errors='ignore') as f:
            #Write the title into the text file
            f.write(url+"\n")
            f.write(soup.title.get_text()+"\n")
            #Then write the whole textblock into the file
            for text in text_blocks:
                text = text.get_text()
                f.write(text+"\n")
def write_urltext_into_file_2(url,path,i,key):
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
        text_blocks = soup.find_all(['p','b'])
        #Create new text file to store the article
        filename=key+" "+str(i)+".txt"
        path_file = os.path.join(path,filename)
        with open(path_file,'w',encoding='utf8',errors='ignore') as f:
            #Write the title into the text file
            f.write(url+"\n")
            f.write(soup.title.get_text()+"\n")
            #Then write the whole textblock into the file
            prev_text=""
            for text in text_blocks:
                text = text.get_text()
                if text.strip()==prev_text.strip():
                    continue
                else:
                    prev_text=text
                f.write(text+"\n")
def write_urltext_into_file_3(url,path,i,key):
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
        text_blocks = soup.find_all(['p','h2','h3'])
        #Create new text file to store the article
        filename=key+" "+str(i)+".txt"
        path_file = os.path.join(path,filename)
        with open(path_file,'w',encoding='utf8',errors='ignore') as f:
            #Write the title into the text file
            f.write(url+"\n")
            f.write(soup.title.get_text()+"\n")
            #Then write the whole textblock into the file
            prev_text=""
            for text in text_blocks:
                text = text.get_text()
                if text.strip()==prev_text.strip():
                    continue
                else:
                    prev_text=text
                f.write(text+"\n")
def check_if_textblock(url):
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
        if not text_blocks:
            return False
        else:
            return True

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
            txt = r.text
            soup = BeautifulSoup(txt, features='lxml')
            headlines = soup.find_all('a', class_=re.compile("PromoLink"))
            if not headlines:
                break
            for headline in headlines:
                link = headline['href']
                if 'programmes' in link and 'news' not in link:
                    continue
                elif ('blogs' in link) or ('/newsround/' in link):
                    continue
                elif ('sport' in link) or ('learningenglish' in link):
                    continue
                elif ('live' in link) or ('/av/' in link):
                    continue
                else:
                    #There are websites with guide in the url that do not open
                    #so check if urls with guide open
                    relevant_url = False
                    good_url = True
                    if 'guides' in link:
                        good_url = try_url(link)
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
                    if '.stm' in link or 'bitesize' in link:
                        good_url=True
                    else:
                        if check_if_textblock(link):
                            good_url = True
                        else:
                            good_url=False
                    relevant_url=True
                    if good_url==True and relevant_url==True:
                        link_list.append(link)
            p+=1
    num_pages.append(p)
    num_articles.append(len(link_list))
    link_dict[key] = link_list.copy()
for element in link_dict:
    if len(link_dict[element])>=100:
        link_dict[element]=link_dict[element][:100]

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
        if '.stm' in url:
            write_urltext_into_file_2(url, path, i,key)
        elif 'bitesize' in url:
            write_urltext_into_file_3(url, path, i, key)
        else:
            write_urltext_into_file(url,path,i,key)    

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
#FUNCTIONS USED TO CALCULATE THE SIMILARITY BETWEEN TWO KEYWORDS#############################
#Function to calculate the pearson correlation between two keywords i and j

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
def calculate_cosine_similarity(matrix,new_matrix):
    for i in range(len(matrix)):
        x = matrix[i]
        for j in range(len(matrix)):
            y=[matrix[l][j] for l in range(len(matrix))]
            new_matrix[i][j]=cosine_similarity(x,y)
    return new_matrix
def calculate_cosine_similarity_dataframe(df,new_df):
    for index1, row1 in df.iterrows():
        #print(row1)
        x=row1
        for index2, row2 in df.iterrows():
            y=row2
            new_df.at[index1,index2]=cosine_similarity(x,y)
#METHOD 1.1 TO FIND THE SIMILARITY BETWEEN WORDS##
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
###############################################################################################################
#METHOD 1.2 TO FIND THE SIMILARITY BETWEEN WORDS##
##->LATER ADD BOTH TOGETHER##
#Work with wikipedia articles
#Find how often the other keywords are mentioned in the wikipedia articles
url_wikipedia = 'https://en.wikipedia.org/wiki/'
occur_matrix_2 = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
i=0
for key in keywords:
    if key=='malicious bot':
        key = 'internet bot'
    j=0
    for other_key in keywords:
        key_in_wikipedia = check_if_word_in_wikipedia_website(url_wikipedia+key,other_key)
        occur_matrix_2[i][j]=key_in_wikipedia
        j+=1
    i+=1

####################################################################################
##ADD VALUES OF TWO METHODS TOGETHER##
dist_matrix = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
for i in range(len(occur_matrix_2)):
    for j in range(len(occur_matrix_2)):
        dist_matrix[i][j]=(occur_matrix[i][j]+occur_matrix_2[i][j])
##Create a matrix which is symmetric, so that matrix[i][j]==matrix[j][i]
sym_matrix = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
for i in range(len(sym_matrix)):
    for j in range(len(sym_matrix)):
        sym_matrix[i][j]=(dist_matrix[i][j]+dist_matrix[j][i])
##Calculate the similarity between the words by using cosine similarity##
word_sym_matrix = [[0,0,0,0,0,0,0,0,0,0] for i in range(len(keywords))]
word_sym_matrix = calculate_cosine_similarity(sym_matrix,word_sym_matrix)
data_word_similarities = create_dataframe(word_sym_matrix)
#Optionally print the data#
print('METHOD 1 to calculate similarities, resulting dataframe:')
print(data_word_similarities)
##########################################################################
##METHOD 2############################################################
##Do a semantic analysis of the words used in 9 of each article
##Only do it for 9 articles, because only 9 were found for malicious bot
dictionaries = {key:{} for key in keywords}
count = 0
#Go through the contents of 9 articles for each keyword
for key in keywords:
    for file in os.listdir(path):
        if file.startswith(key) and count<9:
            count+=1
            path_file = os.path.join(path,file)
            with open(path_file,'r',encoding='utf8',errors='ignore') as f:
                #read the content line by line
                lines = f.readlines()
                for line in lines:
                    #split the lines into words
                    line = re.sub('[^a-zA-Z\s]', ' ', line)
                    words = line.split()
                    #save them in dictionary, along with occurence count
                    for word in words:
                        if word.islower()==False:
                            word=word.lower()
                        if word in dictionaries[key]:
                            dictionaries[key][word]+=1
                        else:
                            dictionaries[key][word]=1
    count=0
#Make a dataframe for dictionary of each keyword
frames = []
for i in range(len(dictionaries)):
    df = pd.DataFrame(dictionaries[keywords[i]],index=[keywords[i]])
    frames.append(df)
#concatenate all dataframes to huge dictionary, with occurence count of all words
#for each keyword, if word didn't occur for one keyword fillna with 0
concatenated = pd.concat(frames)
concatenated = concatenated.fillna(0)

zero_matrix=[[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0] for i in range(len(keywords))]
articles_SA = create_dataframe(zero_matrix)
calculate_cosine_similarity_dataframe(concatenated,articles_SA)
#Min-max scaling
articles_SA-=min(list(articles_SA.min()))
articles_SA/=(max(list(articles_SA.max()))-min(list(articles_SA.min())))
print('METHOD 2 to calculate similarities, resulting dataframe:')
print(articles_SA)
#############################################################################################################################
##METHOD 3##
##Do a semantic analysis on the wikipedia articles of each keyword
##cut down the number of words to the number of words encountered in the shortest article
##Code is very similar to third method
url_wikipedia = 'https://en.wikipedia.org/wiki/'
dictionaries2 = {key:{} for key in keywords}

for key in keywords:
    k = key
    if key=='malicious bot':
        k = 'internet bot'
    try:
        res = requests.get(url_wikipedia+k,stream=True)
        res.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        #Get the text component of the website
        txt = res.text
        soup = BeautifulSoup(txt, features='lxml')
        content=soup.get_text()
        if len(content)>4802:
            content = content[:4802]
        content = re.sub('[^a-zA-Z\s]', ' ',content)
        words = content.split()
        for word in words:
            if word.islower()==False:
                word=word.lower()
            if word in dictionaries2[key]:
                dictionaries2[key][word]+=1
            else:
                dictionaries2[key][word]=1

frames2 = []
for i in range(len(dictionaries2)):
    df = pd.DataFrame(dictionaries2[keywords[i]],index=[keywords[i]])
    frames2.append(df)

concatenated2 = pd.concat(frames2)
concatenated2 = concatenated2.fillna(0)
zero_matrix=[[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0] for i in range(len(keywords))]
wiki_SA = create_dataframe(zero_matrix)
calculate_cosine_similarity_dataframe(concatenated2,wiki_SA)
#min-max-scaling
wiki_SA-=min(list(wiki_SA.min()))
wiki_SA/=(max(list(wiki_SA.max()))-min(list(wiki_SA.min())))
print('METHOD 3 to calculate similarities, resulting dataframe:')
print(wiki_SA)
################################################################
#Now add all methods together:
similarity = wiki_SA.add(articles_SA,fill_value=0)
similarity/=2
similarity = similarity.add(data_word_similarities)
similarity/=2
##########################################################################
#FINAL STEP: CALCULATE DISTANCE BETWEEN WORDS
#Since similiarity is scaled such that most similar words have word_sym_matrix[i][j]=1
#And least similar words have word_sym_matrix[i][j]=0
#Define distance(i,j)=1-word_sym_matrix[i][j]
distance = 1-similarity
print('FINAL DISTANCE MATRIX: ')
print(distance)
##Save distance in distance.xlsx 
writer = pd.ExcelWriter('./distance.xlsx',engine='xlsxwriter')
distance.to_excel(writer, sheet_name='Sheet1', index=True)
wb = writer.book
ws = writer.sheets['Sheet1']
cell_format = wb.add_format({'bold': True})
cell_format.set_font_color('red')
ws.write('A1','Keywords',cell_format)
writer.save()

## Problem 4
def plot_heatmap(df,title):
    fig = sns.heatmap(df,cmap='BrBG',annot=True,annot_kws={'size':6},linewidths=.5,fmt=".2f")
    fig.get_figure().tight_layout()
    fig.get_figure().savefig(title+".png",dpi=300)
df = pd.read_excel('./distance.xlsx')
df.drop('Keywords',axis=1,inplace=True)
df.rename(index={0:'targeted threat',1:'Advanced Persistent Threat',2:'phishing',3:'DoS attack',
    4:'malware',5:'computer virus',6:'spyware',7:'malicious bot',8:'ransomware',9:'encryption'
    },inplace=True)
plot_heatmap(df,'Distance between keywords')
