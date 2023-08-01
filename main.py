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

def get_page_links(html):

    links = []

    soup = BS(html, "html.parser")
    container = soup.find("div", {"class": "container body-container"})
    main = container.find("div", {"class": "main-content"})
    listing = main.find("div", {"class": "listings-wrapper"})
    posts = listing.find_all("div", {"class": "listing"})
    for post in posts:
        header = post.find("div", {"class": "left-side"})
        # title = header.find("p", {"class": "title"}).text.strip()
        # address = header.find("div", {"class": "address"}).text.strip()
        link = header.find("a").get("href")
        full_link = 'https://www.house.kg'+link
        # price_dol = post.find("div", {"class": "sep main"}).find("div", {"class": "price"}).text.strip()
        # price_som = post.find("div", {"class": "sep main"}).find("div", {"class": "price-addition"}).text.strip()
        # desk = post.find("div", {"class": "description"}).text.strip()
        links.append(full_link)
    return links

def get_post_data(html):
    soup = BS(html, 'html.parser')
    main = soup.find("div", {"class": "main-content"})
    header = main.find("div", {"class": "details-header"})
    title = header.find("div", {"class": "left"}).find("h1").text.strip()
    address = header.find("div", {"class": "address"}).text.strip()
    price_dol = header.find("div", {"class": "sep main"}).find("div", {"class": "price-dollar"}).text.strip()
    price_som = header.find("div", {"class": "sep main"}).find("div", {"class": "price-som"}).text.strip()
    mobel_phone = main.find("div", {"class": "phone-fixable-block"}).find("div", {"class": "number"}).text.strip()
    print(mobel_phone)


def main():
    html = get_html(URL)
    links = get_page_links(html)
    
    for link in links:
        detail_html = get_html(link)
        get_post_data(detail_html)
        


if __name__ == "__main__":
    main()