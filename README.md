# Assignment
*NOTE: My code is located in DataCollection&Cleaning.py and my summative report is in report_data_collection_cleaning.pdf.*

You are asked to investigate distances between those 10 keywords by collecting the data from BBC news, processing and analyzing it. You need to also submit a simple report to explain your algorithm (problem 3) and the visualization of the result(problem 4).
- Problem 1. (20%)
Create a Python program that downloads the webpage content (from BBC news) of the top 100 articles relevant to the given keywords from the following url:
https://www.bbc.co.uk/news
- Problem 2. (20%)
Use BeautifulSoup, a library that facilitates scrapping information from web pages, to collect and process the articles contents. Save each article content to a file.
- Problem 3. (40%)
Create a Python program to calculate the distances between each two keywords which belong to the list of keywords saved in keywords.xlsx. Develop your own algorithm to calculate the distances. You are suggested to use the data you downloaded from BBC news but not limited to those data. You can also use other data collected from other source.
Save the results of this algorithm in another xlsx called distance.xlsx, whose format is as followed.
- Problem 4. (20%)
Use seaborn (http://web.stanford.edu/~mwaskom/software/seaborn/index.html) to visualize the distance between any two keywords.
