import sys
import util 
import requests
from bs4 import BeautifulSoup
import re

args = sys.argv
print(args[1])

from libgen_api import LibgenSearch


book_name = args[1]
author_name = args[2]

metadata = util.get_book_metadata(book_name + ' ' + author_name)
if metadata is not None:
    print('Pages:', metadata['pages'])
else:
    print('No search results found.')


s = LibgenSearch()
author_filters = {"Author": author_name}
titles = s.search_title_filtered(book_name, author_filters, exact_match=False)
print(titles)


all_descriptions = {}
all_isbn_codes = {}
desc_pattern = re.compile(r'.*\bDes\b.*')

for title in titles:
    mirror_links = [title['Mirror_1'], title['Mirror_2'], title['Mirror_3']]
    description_main = None
    isbn_main = None
    
    for link in mirror_links:

            # download the HTML content of the page
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



    # print the results for this title
    print(f'Title: {title["Title"]}')
    if description:
        print(f'Description: {description}')
    if isbn:
        print(f'ISBN: {isbn}')
    
    



# search_results = util.search_google_for_book_pds(book_name)
# for item in search_results:
#     title = item.get('title')
#     link = item.get('link')
#     snippet = item.get('snippet')
    
#     # Print out the search result data
#     print(f'Title: {title}')
#     print(f'Link: {link}')
#     print(f'Snippet: {snippet}')
    

	# 9780593653425, 2022035005, 9780593652886