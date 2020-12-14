import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import io


def main():
    news_url = "https://www.ncl.ac.uk/press/latest/"
    news_file = "news_data.txt"
    scrape_data(news_url, news_file)


def read_news(news_file, url_list):
    text_as_list = []
    with io.open(news_file, "r", encoding="utf-8") as f:
        for line in f:
            text_as_list.append(line)
    organise(text_as_list, url_list)


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
    read_news(news_file, correct_url_list)


def organise(text_as_list, url_list):
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
    list3 = []
    for j in range(len(correct_list)):
        list2 = correct_list[j]
        list2.append(url_list[j])
        list3.append(list2)

    correct_list = list3
    print(len(correct_list))


if __name__ == "__main__":
    main()
