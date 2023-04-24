
import requests
import os 
from dotenv import load_dotenv
load_dotenv()

def get_book_metadata(book_name):
    # Set up the API endpoint and parameters
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': 'intitle:{}'.format(book_name)  # Set the book name as the query
    }

    # Send the API request and retrieve the response
    response = requests.get(url, params=params)
    response_data = response.json()

    # Process the search results
    if 'items' in response_data and len(response_data['items']) > 0:
        # Extract the metadata for the first book in the search results
        book_metadata = response_data['items'][0]['volumeInfo']
        pages = book_metadata.get('pageCount')
        description = book_metadata.get('description')

        # Return the book metadata
        return {'pages': pages, 'description': description}
    else:
        return None
    

def search_google_for_book_pds(book):
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': os.environ['api_key_google'],
        'cx': os.environ['search_engine_id'],  
        'q': f'filetype:pdf ${book}',
        'num': 10  # Set the number of search results to retrieve
    }

    # Send the API request and retrieve the response
    response = requests.get(url, params=params)
    response_data = response.json()

    # Process the search results
    if 'items' in response_data:
        return response_data['items']
    else:
        print('no search results found')
        
    