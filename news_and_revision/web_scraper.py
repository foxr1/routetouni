import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import io


def main():
    news_url = "https://www.ncl.ac.uk/press/latest/"
    news_file = "news_and_revision/news_data.txt"
    news_dict = scrape_data(news_url, news_file)
    print("news dict successfully created")
    print(news_dict)
    return news_dict


def read_news(news_file, url_list):
    text_as_list = []
    with io.open(news_file, "r", encoding="utf-8") as f:
        for line in f:
            text_as_list.append(line)
    news_list = organise(text_as_list, url_list)
    return news_list


def scrape_data(url, news_file):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")

    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    tags = soup.find_all("a")
    url_list = []
    correct_url_list = []
    p = re.compile("/press/articles/latest*")
    for tag in tags:
        url_list.append(tag.get('href'))
    for i in range(len(url_list)):
        if p.match(url_list[i]):
            url_list = url_list[i:i + 20]
            break
    for i in range(len(url_list)):
        pre = "https://www.ncl.ac.uk" + url_list[i]
        correct_url_list.append(pre)

    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    with io.open(news_file, "w", encoding="utf-8") as f:
        f.write(text)
    news_list = read_news(news_file, correct_url_list)
    return news_list


def organise(text_as_list, url_list):
    for i in range(len(text_as_list)):
        if text_as_list[i] == "Latest News\n":
            text_as_list = text_as_list[i + 1:i + 301]
            break

    for g in range(250):
        if text_as_list[g] == 'Writing for The Conversation,\n':
            text_as_list.pop(g)
            text_as_list[g] = 'Writing for The Conversation, ' + text_as_list[g]

    correct_list = []
    new_list = []
    y = 0
    for x in range(200):
        new_list.append(text_as_list[x])
        y = x % 3
        if y == 2:
            correct_list.append(new_list)
            new_list = []
    correct_list = correct_list[0:6]
    list3 = []

    for j in range(len(correct_list)):
        list2 = correct_list[j]
        list2.append(url_list[j])
        list3.append(list2)

    news_list = list3

    news_dict = create_dictionary(news_list)
    return news_dict


def create_dictionary(news_list):
    dictionary = {}
    for i in range(len(news_list)):
        a_list = news_list[i]
        title = {a_list[0]: {"Description": a_list[1], "Date": a_list[2], "URL": a_list[3]}}
        dictionary.update(title)
    return dictionary

# if __name__ == "__main__":
# main()
