import sys
import util 

args = sys.argv
print(args[1])

from libgen_api import LibgenSearch


book_name = args[1]

# metadata = util.get_book_metadata(book_name)
# if metadata is not None:
#     print('Pages:', metadata['pages'])
#     print('Description:', metadata['description'])
# else:
#     print('No search results found.')


s = LibgenSearch()
results = s.search_title(book_name)
print(results)


# search_results = util.search_google_for_book_pds(book_name)
# for item in search_results:
#     title = item.get('title')
#     link = item.get('link')
#     snippet = item.get('snippet')
    
#     # Print out the search result data
#     print(f'Title: {title}')
#     print(f'Link: {link}')
#     print(f'Snippet: {snippet}')
    

