import sys
sys.path.append("..")

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv
from utils import get_book_metadata, search_google_for_book_pds, libgen_search_and_scrape, search_pdf_drive_and_scrape, process_array_of_dictionaries, cleaning, extract_urls, final_download_libgen, final_download_pdfdrive, final_download_google, final_webpage_links

load_dotenv()

def search_links(book_name, author_name, top_scores):
    try:
        all_books_found = []
        main_book = []

        # google books metadata 
        metadata = get_book_metadata(book_name, author_name)
        main_book.append(metadata)
        if metadata is None:
            sys.exit('Could not find book in the Google Book Repository. Please check your book and author name')
        else:
            print('Found Metadata in Google Books. Here is the Book found : {title}, {author} , Pages: {page_count}'.format(title=metadata['title'], author=metadata['authors'], page_count=metadata['pageCount']) )
        # google search   
        google_search_results = search_google_for_book_pds(book_name, author_name=author_name)
        if not (google_search_results):
            print('No google search results for some reason')
        else: all_books_found += google_search_results
        print("Google search results found = {number}".format(number=len(google_search_results)))

        #libgen
        book_libgen_found = False   
        libgen_results_ = []
        i = 0
        while (not book_libgen_found or i > 10):
            i += 1
            libgen_results = libgen_search_and_scrape(name=book_name, query='book')
            
            if libgen_results == False:
                book_libgen_found = False
            else:
                
                book_libgen_found = True
                libgen_results_ = libgen_results

        print("Libgen Title books found = {number}".format(number=len(libgen_results_)))
        all_books_found += libgen_results_

        author_libgen_found = False
        libgen_results_2 = 0
        j = 0
        while (author_libgen_found is not True or j > 10):
            j += 1
            libgen_results = libgen_search_and_scrape(name=author_name, query='author')
            if libgen_results == False:
                author_libgen_found = False
            else:
                author_libgen_found = True
                libgen_results_2 = libgen_results

        print("Libgen Author books found = {number}".format(number=len(libgen_results_2)))
        all_books_found += libgen_results_2       



        #pdf drive
        pdf_drive_results = search_pdf_drive_and_scrape(book_name=book_name, author_name=author_name)
        if not (pdf_drive_results):
            print('No pdf drive search results for some reason')
        else: all_books_found += pdf_drive_results
        print("PDF Drive books found = {number}".format(number=len(pdf_drive_results)))

        all_book_strings = process_array_of_dictionaries(all_books_found)
        all_book_strings = list(set(all_book_strings))

        main_book_string = process_array_of_dictionaries(main_book)[0]

        def get_top_matches(main_string, string_array, top_k=5):
            
            model = SentenceTransformer('all-mpnet-base-v2')
            main_string_embedding = model.encode([main_string])
            string_embeddings = model.encode(string_array)
            similarity_scores = cosine_similarity(main_string_embedding, string_embeddings)[0]
            sorted_indices = sorted(range(len(similarity_scores)), key=lambda k: similarity_scores[k], reverse=True)
            top_matches = [(string_array[i], similarity_scores[i]) for i in sorted_indices[:top_k]]

            return top_matches

        top_book_raw = get_top_matches(main_book_string, all_book_strings, int(top_scores))
        similarity_scores = []
        for i in top_book_raw:
            print('Similarity scores: ', i[1])
            similarity_scores.append(float(i[1]))
            
        input_urls = extract_urls(top_book_raw)
        output_list = [tuple(filter(None, tpl)) for tpl in input_urls]
        final_urls = extract_urls(output_list)

        to_download_urls = final_webpage_links(final_urls)
        to_download_urls_final = cleaning(to_download_urls)

        last_urls = []
        for i, url in enumerate(to_download_urls_final):
            if "library.lol" in url:
                last_urls.append(final_download_libgen(url))
            elif "pdfdrive" in url:
                last_urls.append(final_download_pdfdrive(url))
            else:
                last_urls.append(final_download_google(url))

        return last_urls, similarity_scores
    except Exception as e:
        print(e)
        return False,  []


