from flask import Flask, render_template, request
from search import search, vectorizer, tfidf_matrix, filenames, url_to_document, tokenized_documents, stopword_lists
import time

app = Flask(__name__)
app.config['STATIC_URL_PREFIX'] = '/static'


# Initialize start_time globally
start_time = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def perform_search():
    global start_time  # Use the global variable
    query = request.form['search_query']
    
    if start_time is None:
        start_time = time.time()

    results, query_tokens = search(query, vectorizer, tfidf_matrix, filenames, url_to_document, tokenized_documents, stopword_lists)
    end_time = time.time()

    num_documents_found = len(results)
    word_search = ' '.join(query_tokens)
    search_time = end_time - start_time
    run_time = time.time() - start_time

    # Reset start_time for the next search
    start_time = None

    return render_template('index.html', results=results, word_search=word_search, word_hits=num_documents_found, search_time=search_time, run_time=run_time)

if __name__ == '__main__':
    app.run(debug=True)
