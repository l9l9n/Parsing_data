import requests
from bs4 import BeautifulSoup as BS



file = open('test.html', encoding='utf-8')

html = file.read()
soup = BS(html, 'html.parser')

container = soup.find('div', {"class": "container"}).find('div', {"class": "navigation-container"})
ul_list_container = container.find("ul", {"class": "menu"})
li_list = ul_list_container.find_all('li')

for li in li_list:
    print(li.get_text())