import urllib
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
import requests
import fileinput
import wget
import html2text
from urllib.request import urlopen
from bs4 import BeautifulSoup
import io


def main():
    news_url = "https://www.ncl.ac.uk/press/latest/"
    scrape_data(news_url)


def read_news():
    text_as_list = []
    with io.open("news_data.txt", "r", encoding="utf-8") as f:
        for line in f:
            text_as_list.append(line)
    organise(text_as_list)


def scrape_data(url):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()

    text = soup.get_text()

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    with io.open("news_data.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    read_news()


def organise(text_as_list):
    global new_list
    for i in range(len(text_as_list)):
        if text_as_list[i] == "Latest News\n":
            text_as_list = text_as_list[i + 1:i + 301]
            break
    print(text_as_list)
    correct_list = []
    new_list = []
    print(len(text_as_list))
    y = 0
    for x in range(300):
        new_list.append(text_as_list[x])
        y = x % 3
        if y == 2:
            correct_list.append(new_list)
            new_list = []
    correct_list = correct_list[0:20]
    print(correct_list)


if __name__ == "__main__":
    main()
