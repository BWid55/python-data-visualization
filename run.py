#! /usr/bin/python3
import requests
import bs4
import time
import re

start_time = time.time()

#Function to remove html tags while leaving text between them
def remove_html_tags_and_sort_words(html,source):
    text = re.compile(r"[^\w\s]").sub("",re.compile(r"<[^>]*>").sub("",str(html).lower())).split(" ")
    if source == 'nyr':
        for word in text:
            if word in nyr_word_tally:
                nyr_word_tally[word] += 1
            else:
                nyr_word_tally[word] = 1
    elif source == 'fox':
        for word in text:
            if word in fox_word_tally:
                fox_word_tally[word] += 1
            else:
                fox_word_tally[word] = 1

#Set blank asset containers and utility data
desired_number_of_words = 50
words_to_not_use = ["", "\n", "no", "found", "such", "here", "also", "those", "because", "since", "just", "month", "week", "year", "months", "change", "first", "second", "third", "now", "new", "even", "me", "still", ",", ", ", "other", "fox", "new", "through", "told", "news", "per", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "us", "1", "2", "3", "4", "5", "6", "7", "8", "9", "after", "said", "more", "the", "at", "there", "some", "my", "of", "be", "use", "her", "than", "and", "this", "an", "would", "a", "have", "each", "to", "from", "which", "like", "been", "in", "or", "she", "him", "is", "do", "into", "who", "you", "had", "how", "that", "by", "their", "has", "its", "it's", "it", "if", "he", "but", "will", "find", "was", "not", "for", "what", "down", "on", "all", "about", "go", "day", "are", "were", "out", "see", "did", "as", "we", "many", "get", "with", "when", "then", "come", "came", "his", "your", "them", "they", "can", "these", "could", "i", "so"]

fox_article_links_list = []
nyr_article_links_list = []
fox_article_list = []
nyr_article_list = []
fox_word_tally = {}
nyr_word_tally = {}
fox_popular_words = []
nyr_popular_words = []

#Retrieve top 3 Fox News news article links
foxRes = requests.get('https://www.foxnews.com/')
foxRes.raise_for_status()
fox_article_links_list.append(bs4.BeautifulSoup(foxRes.text,'html.parser').select('.main-content .story-1 > .info > .info-header > .title > a')[0].get('href'))
fox_article_links_list.append(bs4.BeautifulSoup(foxRes.text,'html.parser').select('.main-content .story-2 > .info > .info-header > .title > a')[0].get('href'))
fox_article_links_list.append(bs4.BeautifulSoup(foxRes.text,'html.parser').select('.main-content .story-3 > .info > .info-header > .title > a')[0].get('href'))

#Retrieve top 3 New Yorker news article links
nyrRes = requests.get('https://www.newyorker.com/news')
nyrRes.raise_for_status()
nyr_article_links_list.append(bs4.BeautifulSoup(nyrRes.text,'html.parser').select('.Hero__heroWrapper___2CMSF > a')[0].get('href'))
nyr_article_links_list.append(bs4.BeautifulSoup(nyrRes.text,'html.parser').select('.River__riverItem___3huWr .Link__link___3dWao')[1].get('href'))
nyr_article_links_list.append(bs4.BeautifulSoup(nyrRes.text,'html.parser').select('.River__riverItem___3huWr')[1].select('a')[1].get('href'))

#Retrieve top 3 Fox News news articles
for link in fox_article_links_list:
    article = requests.get(link)
    article.raise_for_status()
    fox_article_list.append(article)

#Retrieve top 3 New Yorker news articles
for link in nyr_article_links_list:
    article = requests.get('https://www.newyorker.com' + link)
    article.raise_for_status()
    nyr_article_list.append(article)

#Complete Tally of Fox News Text
for article in fox_article_list:
    article_text = bs4.BeautifulSoup(article.text,'html.parser').select('.article-body')
    for section in article_text:
        remove_html_tags_and_sort_words(section,'fox')

#Complete Tally of New Yorker Shown and Paywall Text
for article in nyr_article_list:
    article_text_shown = bs4.BeautifulSoup(article.text,'html.parser').select('.has-dropcap.has-dropcap__lead-standard-heading')
    article_text_paywall = bs4.BeautifulSoup(article.text,'html.parser').select('.paywall')
    for section in article_text_shown:
        remove_html_tags_and_sort_words(section,'nyr')
    for section in article_text_paywall:
        remove_html_tags_and_sort_words(section,'nyr')

#Most Popular Words Tally for Fox News
while len(fox_popular_words) < desired_number_of_words:
    if (max(fox_word_tally, key=fox_word_tally.get) in words_to_not_use):
        fox_word_tally.pop(max(fox_word_tally, key=fox_word_tally.get))
    else:
        fox_popular_words.append(max(fox_word_tally, key=fox_word_tally.get))
        fox_word_tally.pop(max(fox_word_tally, key=fox_word_tally.get))

#Most Populars Words Tally for The New Yorker
while len(nyr_popular_words) < desired_number_of_words:
    if (max(nyr_word_tally, key=nyr_word_tally.get) in words_to_not_use):
        nyr_word_tally.pop(max(nyr_word_tally, key=nyr_word_tally.get))
    else:
        nyr_popular_words.append(max(nyr_word_tally, key=nyr_word_tally.get))
        nyr_word_tally.pop(max(nyr_word_tally, key=nyr_word_tally.get))

#Creating an HTML file
Func = open("/home/pi-guy/Scripts/py-pro/index.html","w")
#Adding input data to the HTML file
Func.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Stats</h1>
    <br>
    <h2>3 Most Popular Fox News Words</h2>
    <p>They are {fox_first}, {fox_second}, and {fox_third}.<p>
    <br>
    <h2>3 Most Popular The New Yorker Words</h2>
    <p>They are {nyr_first}, {nyr_second}, and {nyr_third}.<p>
    <br>
    <p>Last executed: {execution_time}</p>
    <p>Last execution duration: {execution_duration} seconds</p>
</body>
</html>
""".format(fox_first=fox_popular_words[0], fox_second=fox_popular_words[1], fox_third=fox_popular_words[2], nyr_first=nyr_popular_words[0], nyr_second=nyr_popular_words[1], nyr_third=nyr_popular_words[2], execution_time=time.ctime(), execution_duration=(time.time() - start_time)))
#Saving the data into the HTML file
Func.close()

#Print for crontab log file and debugging
'''
print(fox_article_links_list)
print(nyr_article_links_list)
print(fox_article_list)
print(nyr_article_list)
print(fox_word_tally)
print(nyr_word_tally)
print(fox_popular_words)
print(nyr_popular_words)
'''
print("Successful execution on {execution_time} with a duration of {execution_duration} seconds.".format(execution_time=time.ctime(), execution_duration=(time.time() - start_time)))


#MORE IDEAS TO BUILD OUT PROJECT
#Total words in all 3 articles per media source
#Totals for top words for each media souce
