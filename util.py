
import requests
import os 
from dotenv import load_dotenv
import re, requests
from bs4 import BeautifulSoup
from libgen_api import LibgenSearch

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
        

def libgen_search_and_scrape(book_name, author_name, all_titles):
    s = LibgenSearch()
    author_filters = {"Author": author_name}
    titles = s.search_title_filtered(book_name, author_filters, exact_match=False)
    print(titles)

    link_pattern =  r"https?://[^\s]*library\.lol[^\s]*"

    for title in titles:
        description_main = None
        isbn_main = None
        try: 
            mirror_links = [title['Mirror_1'], title['Mirror_2'], title['Mirror_3']]
            for link in mirror_links:

                if (re.search(link_pattern, link)):
                # download the HTML content of the page
                    print(link, title)
                    response = requests.get(link)
                    response.raise_for_status()
                    
                    html_content = response.content
                    soup = BeautifulSoup(html_content, 'html.parser')
                    # print(soup)
                    # extract description and isbn
                    # description = soup.find('div', string='Description:').find_next_sibling('br').text
                    
                    if isbn_main is None:   
                        isbn = soup.find(lambda tag: "ISBN" in tag.string if tag.string else False).text.split(':')[1].strip() #http://library.lol/main/178EFA8D7182F64E6ACA15457C430745
                        print(isbn)
                        isbn_main = isbn
                    if description_main is None:
                        description = soup.find(string=re.compile("Description")).find_parent().text #library.lol/main
                        print(description)
                        description_main = description
        except Exception:
            print('Error', Exception)
            
        return_array = []
        if description_main is not None:
            return_array.append(description_main)
        if isbn_main is not None:
            return_array.append(isbn_main)
        return return_array
                                    
        