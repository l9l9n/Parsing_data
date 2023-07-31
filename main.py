import requests
from bs4 import BeautifulSoup as BS


URL = "https://www.house.kg/snyat-kvartiru?region=1&town=2&sort_by=upped_at+desc"

def get_html(url):
    response = requests.get(url)
    # html = response.text
    # print(html, 'html.parser')
    if response.status_code == 200:
        return response.text
    return None

def get_page(html):
    soup = BS(html, "html.parser")
    container = soup.find("div", {"class": "container body-container"})
    main = container.find("div", {"class": "main-content"})
    listing = main.find("div", {"class": "listings-wrapper"})
    posts = listing.find_all("div", {"class": "listing"})
    for post in posts:
        header = post.find("div", {"class": "left-side"})
        title = header.find("p", {"class": "title"}).text.strip()
        address = header.find("div", {"class": "address"}).text.strip()
        link = header.find("a").get("href")
        full_link = 'https://www.house.kg'+link
        price_dol = post.find("div", {"class": "sep main"}).find("div", {"class": "price"}).text.strip()
        price_som = post.find("div", {"class": "sep main"}).find("div", {"class": "price-addition"}).text.strip()
        desk = post.find("div", {"class": "description"}).text.strip()
        print(desk)


def main():
    html = get_html(URL)
    if html:
        get_page(html)


if __name__ == "__main__":
    main()