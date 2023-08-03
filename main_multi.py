import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import xlsxwriter
from multiprocessing import Pool



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
    descrip_title = main.find("div", {"class": "description"})
    descrip_title = descrip_title.text.strip() if descrip_title else "Нет описания!"
    # print(descrip_title)

    # description = descrip_title.find("h").strip()
    # print(descrip_title)

    info = main.find('div',{'class':'details-main'}).find_all('div',{'class':'info-row'})
    
    add_info = {}

    for infos in info:
        key = infos.find("div", {"class": "label"}).text.strip()
        value = infos.find("div", {"class": "info"}).text.strip()
        add_info.update({key: value})
    # print(add_info)

    data = {
        'title': title,
        'address': address,
        'dollar': price_dol,
        'som': price_som,
        'phone': mobel_phone,
        'desc': descrip_title,
    }
    return data


def write_excel(data):
    workbook = xlsxwriter.Workbook('test_house.kg.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    column = 0
    for value in data.values():
        worksheet.write(row, column, value)

        row += 1
        
    workbook.close()


def get_last_page(html):
    soup = BS(html, "html.parser")
    page = soup.find("ul", {"class": "pagination"})
    page_list = page.find_all("a", {"class": "page-link"})
    last_page = page_list[-1].get("data-page")
    return int(last_page)


def multi_pars(page_num):
    URL = 'https://www.house.kg/snyat-kvartiru?region=1&town=2&sort_by=upped_at+desc'
    
    page_url = URL + f'&page={page_num}'
    print(page_num)
    html = get_html(page_num)
    links = get_page_links(html)
    for link in links:
        detail_html = get_html(link)
        data = get_post_data(detail_html)
        write_excel(data)
    
def main():
    start = datetime.now()
    URL = 'https://www.house.kg/snyat-kvartiru?region=1&town=2&sort_by=upped_at+desc'
    last_page = get_last_page(get_html(URL))
    html = get_html(URL)
    
    end = datetime.now()
    result = end - start
    print(result)

    
if __name__ == "__main__":
    main()