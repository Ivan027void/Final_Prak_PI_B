# search.py
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
from scipy import sparse
import time
from pre_tfidf import vectorizer
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords

def load_custom_stopwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(file.read().splitlines())

def remove_stopwords_and_stem(tokens, stopword_lists):
    stop_words = set()
    for stopword_list in stopword_lists:
        stop_words.update(stopword_list)
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    return [stemmer.stem(token.lower()) for token in tokens if token.lower() not in stop_words]

def search(query, vectorizer, tfidf_matrix, filenames, url_to_document, tokenized_documents, stopword_lists):
    # Tokenize, remove stopwords, and stem the query
    query_tokens = remove_stopwords_and_stem([word for word in query.split()], stopword_lists)

    # Create a query vector using the same vectorizer
    query_vector = vectorizer.transform([' '.join(query_tokens)])

    # Calculate cosine similarity
    similarity = cosine_similarity(query_vector, tfidf_matrix)[0]

    # Filter results based on cosine similarity and word presence
    relevant_indices = [i for i, sim in enumerate(similarity) if sim > 0]
    filtered_results = [
        {
            'filename': filenames[i],
            'url': url_to_document.get(filenames[i], ''),
            'similarity': similarity[i],
            'found_words': [word for word in query_tokens if word in tokenized_documents[i]['tokens']]
        }
        for i in relevant_indices if any(word in tokenized_documents[i]['tokens'] for word in query_tokens)
    ]

    # Sort results by similarity (higher first)
    filtered_results = sorted(filtered_results, key=lambda x: x['similarity'], reverse=True)

    return filtered_results , query_tokens

# Load TF-IDF matrix and filenames
with open('tfidf_matrix.npz', 'rb') as npz_file:
    tfidf_matrix = np.load(npz_file)
    tfidf_matrix = sparse.csr_matrix((tfidf_matrix['data'], tfidf_matrix['indices'], tfidf_matrix['indptr']),
                                     shape=tfidf_matrix['shape'])

with open('filenames.json', 'r', encoding='utf-8') as filenames_file:
    filenames = json.load(filenames_file)

# Load URL-to-document mapping
with open('url_to_document.json', 'r', encoding='utf-8') as url_file:
    url_to_document = json.load(url_file)

# Load tokenized documents
with open('tokenized_documents.json', 'r', encoding='utf-8') as tokenized_file:
    tokenized_documents = json.load(tokenized_file)

# Load custom stopwords
custom_stopwords = load_custom_stopwords('stopwords.txt')

# Load Sastrawi stopwords
factory = StopWordRemoverFactory()
sastrawi_stopwords = factory.get_stop_words()

# Load NLTK Indonesian stopwords
nltk_stopwords = set(stopwords.words('indonesian'))

# Combine stopwords
stopword_lists = [custom_stopwords, sastrawi_stopwords, nltk_stopwords]
