import sys
import util 
import requests
from bs4 import BeautifulSoup

args = sys.argv
print(args[1])


book_name = args[1]
author_name = args[2]

metadata = util.get_book_metadata(book_name + ' ' + author_name)
if metadata is not None:
    print('Pages:', metadata['pages'])
else:
    print('No search results found.')


pdf_drive_url = f'https://www.pdfdrive.com/search?q={book_name} {author_name}&searchin=&pagecount=&pubyear=&orderby='
pdf_drive_page = requests.get(pdf_drive_url)

soup = BeautifulSoup(pdf_drive_page.content, 'html.parser')
results = soup.findAll('a', attrs={'class': 'ai-search'})

for i, result in enumerate(results):
    print(i, result.parent)
    pagecount = result.parent.find('span', {'class': 'fi-pagecount'})
    print(pagecount.text)
    print('-----------------------------------------')
    title = result.find('h2').text
    link = 'https://www.pdfdrive.com'+ result['href']
    # print(i, title, '-', link)
        
    # search_results = util.search_google_for_book_pds(book_name)
# for item in search_results:
#     title = item.get('title')
#     link = item.get('link')
#     snippet = item.get('snippet')
    
#     # Print out the search result data
#     print(f'Title: {title}')
#     print(f'Link: {link}')
#     print(f'Snippet: {snippet}')
    