"""
Name: William Macpherson
This python file web scrapes off the https://www.ncl.ac.uk/press/latest/ website for information about recent news
related to newcastle and newcastle university.


Functions
----------
main():
    contains the file location and the url to the latest news on newcastles website

read_news(news_file, url_list):
    reads the news_file and adds each line to a list to be parsed to organise function

scrape_data(url, news_file):
    scrapes the website for all information and saves to a file locally, also saves all href's in a list to be appended
    to a dictionary later

organise(text_as_list, url_list):
    organises the list containing each line of text scraped from the website into a list of lists with the inner
    list containing 4 items (title, description, date, url), also contains some error handling

create_dictionary(news_list):
    re-formats the news_list '[list[list]]' to a dictionary format for easy of us in jinja and html


"""
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


# Runs the program when called with the appropriate text file and url for the website that is scraped
def main():
    news_url = "https://www.ncl.ac.uk/press/latest/"
    news_dict = scrape_data(news_url)
    # Returns a dictionary of the news articles
    return news_dict


def scrape_data(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    tags = soup.find_all("a")

    # Finds the URL's that relate to each news article
    url_list = []
    correct_url_list = []
    p = re.compile("/press/articles/latest*")
    for x in tags:
        url_list.append(x.get('href'))
    for i in range(len(url_list)):
        if p.match(url_list[i]):
            # Caps the list of URL's to 20
            url_list = url_list[i:i + 20]
            break
    for i in range(len(url_list)):
        # Recreates the URLs to the correct format so they can be clicked on the website
        pre = "https://www.ncl.ac.uk" + url_list[i]
        correct_url_list.append(pre)
    # Strips down the strings taking out black spaces and adding new lines formatting
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # Adds each line of text into a file
    text_as_list = text.split('\n')
    news_list = organise(text_as_list, correct_url_list)
    return news_list


def organise(text_as_list, url_list):
    for i in range(len(text_as_list)):
        if text_as_list[i] == "Latest News":
            text_as_list = text_as_list[i + 1:i + 301]
            break
    # Error handling with all articles starting with 'Writing for The Conversation,' due to the title being
    # separate items on the list
    for g in range(250):
        if text_as_list[g] == 'Writing for The Conversation,':
            text_as_list.pop(g)
            text_as_list[g] = 'Writing for The Conversation, ' + text_as_list[g]
    correct_list = []
    new_list = []
    y = 0
    # Begins to break up large text_as_list list into correct format of list of lists with each list containing just
    # the title, description, date
    for x in range(200):
        new_list.append(text_as_list[x])
        y = x % 3
        if y == 2:
            correct_list.append(new_list)
            new_list = []
    # Caps the list size to 6 due to only 6 flipcards shown on the page
    correct_list = correct_list[0:6]
    list3 = []
    # Adds the url corresponding to each article to the list of lists
    for j in range(len(correct_list)):
        list2 = correct_list[j]
        list2.append(url_list[j])
        list3.append(list2)
    news_list = list3
    news_dict = create_dictionary(news_list)
    # Returns the news_dictionary
    return news_dict


def create_dictionary(news_list):
    # Due to formatting in html page and jinja, converts the list of lists into a dictionary of dictionary format
    dictionary = {}
    for i in range(len(news_list)):
        flip_card_id = "flip-card-" + str(i + 1)
        a_list = news_list[i]
        title = {a_list[0]: {"Description": a_list[1], "Date": a_list[2], "URL": a_list[3], "ID": flip_card_id}}
        dictionary.update(title)
    return dictionary