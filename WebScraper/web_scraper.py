from bs4 import BeautifulSoup
from urllib.request import urlopen
def main():
    url="https://www.ncl.ac.uk/press/latest/"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    soup.replace()
    print(soup.get_text())

if __name__=="__main__":
    main()