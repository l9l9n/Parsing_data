import requests
from bs4 import BeautifulSoup as BS


URL = "https://www.house.kg/snyat-kvartiru?region=1&town=2&sort_by=upped_at+desc"

response = requests.get(URL)
html = response.text
# print(html, 'html.parser')

soup = BS(html, "html.parser")
container = soup.find("div", {"class": "container body-container"})
print(container)