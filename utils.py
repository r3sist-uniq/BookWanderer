
import requests
import os 
from dotenv import load_dotenv
import re, requests
from bs4 import BeautifulSoup
from libgen_api import LibgenSearch
import os 


load_dotenv()
api_key_google = os.getenv('API_KEY_GOOGLE')
search_engine_id = os.getenv('SEARCH_ENGINE_ID')

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
        # Return the book metadata
        return book_metadata
    else:
        return None
    

def search_google_for_book_pds(book):
    books_found = []
    url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': api_key_google,
        'cx': search_engine_id,  
        'q': f'filetype:pdf ${book}',
        'num': 10  # Set the number of search results to retrieve
    }
    
    # Send the API request and retrieve the response
    response = requests.get(url, params=params)
    response_data = response.json()

    # Process the search results
    if 'items' in response_data:
        for item in response_data['items']:
            title = item.get('title')
            link = item.get('link')
            snippet = item.get('snippet')
            book = {'title': title, 'link': link, 'snippet': snippet, 'source': 'google search'}
            books_found.append(book)
        
        return books_found
    else:
        print('no google search results found')                                  

def search_pdf_drive_and_scrape(book_name, author_name):
    all_books = []
    pdf_drive_url = f'https://www.pdfdrive.com/search?q={book_name} {author_name}&searchin=&pagecount=&pubyear=&orderby='
    pdf_drive_page = requests.get(pdf_drive_url)

    soup = BeautifulSoup(pdf_drive_page.content, 'html.parser')
    results = soup.findAll('a', attrs={'class': 'ai-search'})

    for i, result in enumerate(results):
        everything = result.parent.text.split() #everything - pages, title, and description some
        link = 'https://www.pdfdrive.com'+ result['href'] #link
        
        book = {'title': " ".join(everything), link: link, 'source': 'pdf drive'}
        all_books.append(book)

    return all_books



def create_string_out_of_dictionary(dictionary):
    result = ""
    for key, value in dictionary.items():
        if isinstance(value, dict):
            result += str(key)+ " " + create_string_out_of_dictionary(value) + " "
        else:
            result += str(key) + " " + str(value) + " "
    return result.strip()

def process_array_of_dictionaries(array):
    result_array = []
    for dictionary in array:
        result_string = create_string_out_of_dictionary(dictionary)
        result_array.append(result_string)
    return result_array


def libgen_search_and_scrape(name, query):
    s = LibgenSearch()
    all_books = []
    if query == 'author':
        titles = s.search_author(name)
    elif query == 'book':
        titles = s.search_title(name)
    
    link_pattern =  r"https?://[^\s]*library\.lol[^\s]*"

    for title in titles:
        description_main = None
        isbn_main = None
        try: 
            mirror_links = [title['Mirror_1'], title['Mirror_2'], title['Mirror_3']]
            for link in mirror_links:

                if (re.search(link_pattern, link)):
                # download the HTML content of the page
                    response = requests.get(link)
                    response.raise_for_status()
                    
                    html_content = response.content
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    if isbn_main is None:   
                        isbn = soup.find(lambda tag: "ISBN" in tag.string if tag.string else False).text.split(':')[1].strip() #http://library.lol/main/178EFA8D7182F64E6ACA15457C430745
                        isbn_main = isbn
                    if description_main is None:
                        description = soup.find(string=re.compile("Description")).find_parent().text #library.lol/main
                        description_main = description
        except Exception:
            pass
            # print('Error in Libgen', Exception)
            
        book = title.copy()
        book['source'] = 'libgen'
        if description_main is not None:
            book['description'] = description_main
        if isbn_main is not None:
            book['isbn'] = isbn_main
        all_books.append(book)
    
    return all_books

def extract_urls(arr):
    urls = []
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    
    for tup in arr:
        url_tuple = []
        for string in tup:
            if isinstance(string, str):
                found_urls = re.findall(regex, string)
                for url in found_urls:
                    extracted_url = re.search("(?P<url>https?://[^\s]+)", url[0]).group("url")
                    url_tuple.append(extracted_url)
        urls.append(tuple(url_tuple))
    return urls

def final_webpage_links(arr): 
    to_download_urls = []
    for i, urls in enumerate(arr):
        for url in urls:
            response = requests.head(url)
            if response.status_code == 200:
                print(f"Downloading file from {url}")
                to_download_urls.append(url)
                break
        else:
            print(f"No link works from tuple number {i+1}")
    return to_download_urls




def cleaning(bad_urls):
    updated_links = []
    for link in bad_urls:
        if "pdfdrive" in link:
            updated_links.append(link.replace("-e", "-d"))
        else:
            updated_links.append(link)
    return updated_links





def final_download_libgen(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    ul_element = soup.find("ul")
    li_element = ul_element.find("li")
    a_element = li_element.find("a")
    final_link = a_element["href"]
    print(final_link)

def final_download_pdfdrive(link):
    return

def final_download_google(link):
    return





















