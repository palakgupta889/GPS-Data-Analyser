from bs4 import BeautifulSoup as Soup

html = "output1.html"
soup = Soup(open(html), "html.parser")

mydivs = soup.find("div", {"id": "legend"})

print(soup)