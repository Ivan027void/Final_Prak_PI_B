import requests
import os
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

# Create the 'downloadhtml' directory if it doesn't exist
if not os.path.exists('downloadhtml'):
    os.makedirs('downloadhtml')

# Function to download HTML from a given URL and save it to a file
def download_html(url, filename, user_agent):
    try:
        headers = {'User-Agent': user_agent}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f'Successfully downloaded: {filename}')
            return True
        else:
            print(f'Failed to download: {filename}')
    except Exception as e:
        print(f'Error downloading {filename}: {str(e)}')
    return False

# Function to process links from a file
def process_links(file_name, start_id, max_count, user_agents, sort_link_file):
    current_id = start_id
    downloaded_count = 0

    with open(file_name, 'r') as file:
        links = file.read().splitlines()

    user_agent_index = 0  # Index to track the current user agent
    for link in links:
        if downloaded_count >= max_count:
            break  # Stop when 2000 HTML files are downloaded for each document
        # Get the content of the HTML page
        filename = f'downloadhtml/{current_id}_{link.split("/")[-1]}.html'
        user_agent = user_agents[user_agent_index]
        if download_html(link, filename, user_agent):
            current_id += 1
            downloaded_count += 1
            with open(sort_link_file, 'a') as sort_file:
                sort_file.write(link + '\n')

        # Change user agent every 500 URLs
        if downloaded_count % 500 == 0:
            user_agent_index = (user_agent_index + 1) % len(user_agents)
            time.sleep(2)  # Introduce a delay to avoid being blocked

    return current_id, downloaded_count

# Fake User-Agent generator
ua = UserAgent()

# Generate three different User-Agents for rotation
user_agents = [ua.edge, ua.firefox, ua.chrome]

# Process links for the first document with ID range 1 to 2000
current_id, downloaded_count = process_links('nature_link.txt', 1, 2000, user_agents, 'sort_link.txt')

# Process links for the second document with ID range 2001 to 4000
current_id, downloaded_count = process_links('Pendidikan_link.txt', 2001, 2000, user_agents, 'sort_link.txt')

print(f'Total HTML files downloaded for document 1: {downloaded_count}')
print(f'Total HTML files downloaded for document 2: {downloaded_count}')
