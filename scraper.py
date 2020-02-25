from bs4 import BeautifulSoup
import requests
import csv
import logging

logging.basicConfig(level=logging.INFO)

def get_url(url):
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
                             'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
               'Accept': 'text/html,application/xhtml+xml,application/xml;'
                         'q=0.9,image/webp,*/*;q=0.8'}
    try:
        req = session.get(url, headers=headers).text
    except requests.exceptions.RequestException:
        raise
    return BeautifulSoup(req, 'lxml')

def get_data(soup):
    product_data = []
    for link in soup.findAll('a', {'class': 'thread-title--card'}):
        print('link: ', link['href'])
        product_links.append(link['href'])
        # get product page
        prod = get_url(link['href'])
        # product_pages.append(prod)
        try:
            product_name = prod.find('span', {'class': 'thread-title--item'}).text.strip()
        except:
            product_name = 'None'
        try:
            product_date = prod.find('span', {'class': 'space--fromW3-ml-1 size--all-s space--t-2 space--fromW3-t-0 '
                                                   'overflow--wrap-on space--fromW3-r-2'}).text.strip()
        except:
            product_date = 'None'
        product_comments = prod.find('a', {'class': 'cept-comment-link'}).text.strip()
        try:
            product_votes = prod.find('span', {'class': 'cept-vote-temp'}).text.replace('°', '').strip()
        except AttributeError: # offer not active anymore
            product_votes=0
        try:
            product_merchant = prod.find('span', {'class': 'text--b text--color-brandPrimary '
                                                           'cept-merchant-name'}).text.strip()
        except AttributeError: #no merchant
            product_merchant = 'None'
        product_group_html = prod.findAll('li', {'class': 'carousel-list-item previewList-itemH width--all-6 '
                                                          'width--fromW3-4 width--fromW4-3'})
        product_group = []
        for group in product_group_html:
            product_group.append(group.text)
        product_data.append({'product_name': product_name, 'product_date': product_date, 'product_group': product_group,
                             'product_comments': product_comments, 'product_votes': product_votes,
                             'product_merchant': product_merchant, })
    return product_data


def save_data(product_data):
    # with open('product_links.json', 'a') as f:
    #     json.dump(product_links, fp=f)

    with open('product_data.csv', 'a') as f:
        fieldnames = ['product_name', 'product_date', 'product_group', 'product_comments', 'product_votes',
                      'product_merchant']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(product_data)


def get_pepper_products():
    for i in range(3130, pages_range):
        logging.info(f'PROCESSING PAGE: {str(i)}')
        soup = get_url(main_url+str(i))
        try:
            product_data = get_data(soup)
            if i % 2 == 0:
                save_data(product_data)
        except:
            raise

main_url = 'http://pepper.pl/nowe?page='
pages_range=8379
product_links = []
product_pages = []

# with open('product_data.csv', 'w') as f:
#     fieldnames = ['product_name', 'product_date', 'product_group', 'product_comments', 'product_votes',
#                   'product_merchant']
#     writer = csv.DictWriter(f, fieldnames=fieldnames)
#     writer.writeheader()

get_pepper_products()

