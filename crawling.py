import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

def get_urls(url):
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = []
        for article in soup.find_all('h2', class_='title'):
            link = article.find('a')['href']
            links.append(link)
            
        return links
   
def save_urls(links, category):
    # Create a filename based on the category
    filename = f'{category}_link.txt'

    with open(filename, 'a') as f:
        for link in links:
            f.write(link + '\n')

if __name__ == '__main__':
    # Define the date ranges
    end_date = '2023-11-26'
    start_date_pendidikan = '2022-11-01'
    start_date_nature = '2022-11-01'    
    current_date = end_date  # Start crawling from the most recent date
    links_crawled_pendidikan = 0  # Counter for links crawled from 'pendidikan' category
    links_crawled_nature = 0  # Counter for links crawled from 'nature' category
    switch_category_limit = 3000  # The limit to switch to the 'nature' category

    while current_date >= start_date_nature and (links_crawled_pendidikan + links_crawled_nature) < 6000:
        if links_crawled_pendidikan < switch_category_limit:
            url = 'https://www.kompasiana.com/indeks?page=1&category=pendidikan&date={}'.format(current_date)
            category = 'pendidikan'
        else:
            if links_crawled_nature == 0:
                current_date = end_date
            url = 'https://www.kompasiana.com/indeks?page=1&category=nature&date={}'.format(current_date)
            category = 'nature'
        
        # Get URLs for the current category
        links = get_urls(url)

        # Save URLs to the appropriate file
        save_urls(links, category)

        print(f'{category.capitalize()} links berhasil diambil untuk tanggal {current_date}')

        if category == 'pendidikan':
            links_crawled_pendidikan += len(links)
        else:
            links_crawled_nature += len(links)

        current_date = (datetime.strptime(current_date, '%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Add a delay of a few seconds between requests to avoid overloading the server
        time.sleep(1)  # Adjust the delay as needed
