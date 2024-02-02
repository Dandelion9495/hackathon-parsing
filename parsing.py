import requests
from bs4 import BeautifulSoup as bs
import csv

def get_html(url):
    response = requests.get(url)
    return response.text


def write_to_csv(data):
    with open('data.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow([data['title'], data ['price'], data['image']])


def get_total_pages(html):
    soup = bs(html, 'lxml')
    pages_ul = soup.find('div', class_='pager-wrap').find('ul', class_='pagination pagination-sm')
    last_page = pages_ul.find_all('li')[-1]
    total_pages = last_page.find('a').get('href').split('=')[-1]
    return int(total_pages)


def get_data(html):
    soup = bs(html, 'lxml')
    product_list = soup.find('div', class_="product-index product-index oh").find('div', class_= "list-view")
    products = product_list.find_all('div', class_="item product_listbox oh")
    
    for phones in products:
        try:
            title = phones.find('div', class_="listbox_title oh").find('a').text
            # print(title)
        except:
            title = ''
        try:
            price = phones.find('div', class_="listbox_price text-center").find('strong').text
            # print(price)
        except:
            price = ''
        try:
            image = phones.find('div', class_="listbox_img pull-left").find('a').find('img').get('src')
            # print(image)
        except:
            image = ''
        
        

        data = {
            'title': title,
            'price': price,
            'image': image
        }
        # print(data)
        write_to_csv(data)



def main():
    telefony_url = 'https://www.kivano.kg/mobilnye-telefony'
    pages = '?page='

    total_pages = get_total_pages(get_html(telefony_url))

    # print(total_pages)

    for page in range(1, total_pages+1):
        url_ = telefony_url + pages + str(page)
        # print(url)
        html_ = get_html(url_)
        get_data(html_)


    # get_total_pages(get_html(telefony_url))
    # get_data(get_html(telefony_url))
with open('data.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['title', 'price', 'image'])

main()
