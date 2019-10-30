from bs4 import BeautifulSoup as Soup

html = "map_newest_split.html"
soup = Soup(open(html), "html.parser")

mydivs = soup.find("div", {"id": "legend"})

mydivs.append(str(x))

print(soup)