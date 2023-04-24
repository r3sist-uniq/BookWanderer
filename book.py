import argparse
from googlesearch import search
import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
import numpy as np

def get_top_matches(book_name):
    # Create a SentenceTransformer object to convert book names to embeddings
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    # Search for book in Google's search PDFs and get the URLs of the search results
    query = f"{book_name} filetype:pdf"
    urls = search(query, num_results=10)
    print(urls)
    # Search for book in Libgen and get the URLs of the search results
    libgen_url = f'http://gen.lib.rus.ec/search.php?req={book_name}&open=0&res=25&view=simple&phrase=1&column=def'
    libgen_page = requests.get(libgen_url)
    libgen_soup = BeautifulSoup(libgen_page.content, 'html.parser')
    libgen_results = libgen_soup.select('td[width="500"] a')
    libgen_urls = [result['href'] for result in libgen_results]
    print(libgen_urls)
    # Search for book in pdf drive and get the URLs of the search results
    pdf_drive_url = f'https://www.pdfdrive.com/search?q={book_name}&searchin=&pagecount=&pubyear=&orderby='
    pdf_drive_page = requests.get(pdf_drive_url)
    pdf_drive_soup = BeautifulSoup(pdf_drive_page.content, 'html.parser')
    pdf_drive_results = pdf_drive_soup.select('a.btn-primary')
    pdf_drive_urls = [result['href'] for result in pdf_drive_results]
    print(pdf_drive_urls)
    # Combine all the URLs and remove duplicates
    # urls = list(set(list(urls) + libgen_urls + pdf_drive_urls))

    # Convert the book name to an embedding
    # book_embedding = model.encode([book_name])[0]

    # # Calculate the similarity between the book embedding and each URL's title and description
    # similarities = []
    # for url in urls:
    #     print(url)
    #     page = requests.get(url)
    #     soup = BeautifulSoup(page.content, 'html.parser')
    #     title = None
    #     if soup.title is not None:
    #         title = soup.title.string
    #     description = soup.find('meta', attrs={'name': 'description'})['content']
    #     embedding = model.encode([title, description])[0]
    #     similarity = np.dot(book_embedding, embedding) / (np.linalg.norm(book_embedding) * np.linalg.norm(embedding))
    #     similarities.append(similarity)

    # # Sort the URLs by similarity and return the top 3 matches
    # top_matches = [url for _, url in sorted(zip(similarities, urls), reverse=True)[:3]]
    top_matches = 0;
    return top_matches

if __name__ == '__main__':
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description='Search for a book in various sources')
    parser.add_argument('--book_name', type=str, help='Name of the book to search for')
    args = parser.parse_args()

    # Get the top 3 matches for the book name
    top_matches = get_top_matches(args.book_name)
    print(top_matches)