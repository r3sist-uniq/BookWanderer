import sys
import util 

args = sys.argv

book_name = args[1]
author_name = args[2]
top_scores = args[3]

all_books_found = []
main_book = []


# google books metadata
metadata = util.get_book_metadata(book_name + ' ' + author_name)
main_book.append(metadata)

# google search   
google_search_results = util.search_google_for_book_pds(book_name)
if not (google_search_results):
    print('No google search results for some reason')
else: all_books_found += google_search_results

#libgen
libgen_results = util.libgen_search_and_scrape(book_name=book_name, author_name=author_name)
if not (libgen_results):
    print('No libgen search results for some reason')
else: all_books_found += libgen_results


#pdf drive
pdf_drive_results = util.search_pdf_drive_and_scrape(book_name=book_name, author_name=author_name)
all_books_found += pdf_drive_results
if not (pdf_drive_results):
    print('No pdf drive search results for some reason')
else: all_books_found += pdf_drive_results



all_book_strings = util.process_array_of_dictionaries(all_books_found)
all_book_strings = list(set(all_book_strings))

print(len(all_books_found), 'before removing duplicates')
print(len(all_book_strings), 'after removing duplicates')

main_book_string = util.process_array_of_dictionaries(main_book)[0]
