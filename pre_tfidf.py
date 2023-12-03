# tfidf.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import json

# Load tokenized documents
with open('tokenized_documents.json', 'r', encoding='utf-8') as file:
    tokenized_documents = json.load(file)

# Extract tokens and filenames
documents = [' '.join(doc['tokens']) for doc in tokenized_documents]
filenames = [doc['filename'] for doc in tokenized_documents]

# Create a TF-IDF matrix
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(documents)

# Save TF-IDF matrix and filenames
with open('tfidf_matrix.npz', 'wb') as npz_file:
    np.savez_compressed(npz_file, data=tfidf_matrix.data, indices=tfidf_matrix.indices,
                        indptr=tfidf_matrix.indptr, shape=tfidf_matrix.shape)
with open('filenames.json', 'w', encoding='utf-8') as filenames_file:
    json.dump(filenames, filenames_file)
