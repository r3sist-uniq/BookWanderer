import sys
import utils
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()
args = sys.argv

book_name = args[1]
author_name = args[2]

if args[3] is None:
    top_scores = 3
else: top_scores = args[3]

all_books_found = []
main_book = []

print(book_name, author_name, top_scores)
# google books metadata 
metadata = utils.get_book_metadata(book_name + ' ' + author_name)
main_book.append(metadata)

# google search   
google_search_results = utils.search_google_for_book_pds(book_name)
if not (google_search_results):
    print('No google search results for some reason')
else: all_books_found += google_search_results

#libgen
book_libgen_found = False
libgen_results_ = 0
i = 0
while (not book_libgen_found or i > 10):
    i += 1
    libgen_results = utils.libgen_search_and_scrape(name=book_name, query='book')
    
    if libgen_results == False:
        book_libgen_found = False
        print('wrongg happend', i)
    else:
        
        book_libgen_found = True
        libgen_results_ = libgen_results

all_books_found += libgen_results_

author_libgen_found = False
libgen_results_2 = 0
j = 0
while (author_libgen_found is not True or j > 10):
    j += 1
    libgen_results = utils.libgen_search_and_scrape(name=author_name, query='author')
    if libgen_results == False:
        author_libgen_found = False
        print('wrong happend author', j)
    else:
        author_libgen_found = True
        libgen_results_2 = libgen_results
        
all_books_found += libgen_results_2       


#pdf drive
pdf_drive_results = utils.search_pdf_drive_and_scrape(book_name=book_name, author_name=author_name)
all_books_found += pdf_drive_results
if not (pdf_drive_results):
    print('No pdf drive search results for some reason')
else: all_books_found += pdf_drive_results

print(all_books_found, 'hello')
all_book_strings = utils.process_array_of_dictionaries(all_books_found)
all_book_strings = list(set(all_book_strings))

print(len(all_books_found), 'before removing duplicates')
print(len(all_book_strings), 'after removing duplicates')

main_book_string = utils.process_array_of_dictionaries(main_book)[0]

def get_top_matches(main_string, string_array, top_k=5):
    
    model = SentenceTransformer('all-mpnet-base-v2')
    main_string_embedding = model.encode([main_string])
    string_embeddings = model.encode(string_array)
    similarity_scores = cosine_similarity(main_string_embedding, string_embeddings)[0]
    sorted_indices = sorted(range(len(similarity_scores)), key=lambda k: similarity_scores[k], reverse=True)
    top_matches = [(string_array[i], similarity_scores[i]) for i in sorted_indices[:top_k]]

    return top_matches

top_book_raw = get_top_matches(main_book_string, all_book_strings, int(top_scores))

input_urls = utils.extract_urls(top_book_raw)
output_list = [tuple(filter(None, tpl)) for tpl in input_urls]
final_urls = utils.extract_urls(output_list)

to_download_urls = utils.final_webpage_links(final_urls)
to_download_urls_final = utils.cleaning(to_download_urls)

pakka_final_urls = []
for i, url in enumerate(to_download_urls_final):
    if "library.lol" in url:
        pakka_final_urls.append(utils.final_download_libgen(url))
    elif "pdfdrive" in url:
        pakka_final_urls.append(utils.final_download_pdfdrive(url))
    else:
        pakka_final_urls.append(utils.final_download_google(url))

print(pakka_final_urls)


# TO CHECK IF THE LAST URLS ARE ACTUALLY FROM RESPECTIVE INDEX OF TUPLES
# for i, urls in enumerate(final_urls):
#     if to_download_urls[i] in urls:
#         print(f"true {i+1}st time")
#     else:
#         print("wtf")


# libgen_results = utils.libgen_search_and_scrape(name=book_name, query='book')
# if not (libgen_results):
#     print('No libgen search results for some reason')
# else: all_books_found += libgen_results

# libgen_results_2 = utils.libgen_search_and_scrape(name=author_name, query='author')
# if not (libgen_results_2):
#     print('No libgen search results for some reason')
# else: all_books_found += libgen_results_2
