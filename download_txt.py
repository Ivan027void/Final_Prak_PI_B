import os
import re
import json
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import time

# Function to check if the content is in English and translate it to Indonesian
def translate_to_indonesian(text, max_retries=3):
    translator = Translator()
    retries = 0

    while retries < max_retries:
        try:
            result = translator.translate(text, dest='id').text
            return result

        except Exception as e:
            print(f"Translation error: {str(e)}")
            retries += 1
            time.sleep(2)  # Introduce a delay before retrying

    # If translation fails after max retries, return the original text
    return text

# Make a new directory 'corpus' to handle the text files
corpus_directory = "C:/Users/ahini/Downloads/uas_projek_pi_lab/corpus/"
if not os.path.exists(corpus_directory):
    os.makedirs(corpus_directory)

# Load URLs from 'tes.txt'
with open('sort_link.txt', 'r', encoding='utf-8') as urls_file:
    urls = urls_file.read().splitlines()

# Initialization of variables
url_to_document = {}
skipped_urls = []
error_urls = []  # List to store URLs that encountered errors

# Loop through each URL
for index, url in enumerate(urls, start=1):
    try:
        # Send GET request
        response = requests.get(url)

        # Parse content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find element with itemprop="articleBody"
        article_body = soup.find(itemprop='articleBody')

        # If element not found, skip URL and add to skipped list
        if article_body is None:
            skipped_urls.append(url)
            continue

        # Get text from each <p> element and save to list
        paragraphs = [p.get_text() for p in article_body.find_all('p')]

        # Concatenate list into one string with each paragraph separated by a newline
        text = '\n'.join(paragraphs)

        # Remove non-alphabetic characters and punctuation
        text = re.sub(r'[^\w\s]', ' ', text)

        # Case folding
        text = text.lower()

        # Extract title of the page from the URL
        title_from_url = url.split('/')[-1]

        # Create filename with index and title from the URL
        filename = f"{index}_{title_from_url}.txt"

        # Translate content to Indonesian if it is in English
        if not text.isascii():
            text = translate_to_indonesian(text)

        # Add the URL to the dictionary
        url_to_document[filename] = url

        # Print filename when done
        print(f"Processed: {filename}")

        # Specify directory where you want to save files
        file_path = os.path.join(corpus_directory, filename)

        # Save text to .txt file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)

    except Exception as e:
        # Print error message and add the URL to the error list
        print(f"Error processing {url}: {str(e)}")
        error_urls.append((index, url))
        
# Save error URLs and their indices to a file
with open('error_urls.txt', 'w', encoding='utf-8') as f:
    for index, url in error_urls:
        f.write(f"{index}: \"{url}\",\n")

# Save the dictionary to a file
with open('url_to_document.json', 'w', encoding='utf-8') as f:
    json.dump(url_to_document, f)

# Print skipped URLs
print("Skipped URLs:")
for skipped_url in skipped_urls:
    print(skipped_url)

# Save error URLs and their indices to a file
with open('error_urls.txt', 'w', encoding='utf-8') as f:
    for index, url in error_urls:
        f.write(f"{index}: {url}\n")
