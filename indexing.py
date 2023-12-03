# tokenize.py
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import os
import json
import time

# Set the directory path
corpus_directory = 'corpus/'

# Initialize the stemmer
stemmer = StemmerFactory().create_stemmer()

# Load Sastrawi stopwords
sastrawi_stopwords = StopWordRemoverFactory().get_stop_words()

# Load custom stopwords from your file
custom_stopwords_file = 'stopwords.txt'
with open(custom_stopwords_file, 'r', encoding='utf-8') as file:
    custom_stopwords = [line.strip() for line in file]

# Combine stopwords
stopwords = set(sastrawi_stopwords).union(set(custom_stopwords))

# Tokenized documents
tokenized_documents = []

# Get sorted list of filenames
sorted_filenames = sorted(os.listdir(corpus_directory))

start_time = time.time()
# Loop through each document in the sorted order
for filename in sorted_filenames:
    file_path = os.path.join(corpus_directory, filename)

    # Read the document content
    with open(file_path, 'r', encoding='utf-8') as file:
        document_content = file.read()

    # Remove stopwords, stem, and tokenize
    tokens = [stemmer.stem(word) for word in document_content.split() if word.lower() not in stopwords]
    tokenized_documents.append({'filename': filename, 'tokens': tokens})
    print(f"Tokenized {filename}")

end_time = time.time()
tokenize_time = end_time - start_time
print(f"Tokenization finished in {tokenize_time} seconds")

# Save tokenized documents
with open('tokenized_documents.json', 'w', encoding='utf-8') as output_file:
    json.dump(tokenized_documents, output_file)
