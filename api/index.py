from flask import Flask, request, jsonify, render_template
import search_links

app = Flask(__name__)

@app.route('/links', methods=['GET'])
def search_books():
    
    book_name = request.args.get('book_name')
    author_name = request.args.get('author_name')
    number_of_links = request.args.get('top_links')
    
    if not book_name or not author_name or not number_of_links:
        return jsonify({'error': 'Please send the correct URL params!'}), 400
    
    links_found, similarity_scores = search_links.search_links(book_name=book_name, author_name=author_name, top_scores=number_of_links)
    print(type(similarity_scores))
    if not links_found == False:
        return jsonify({'links': links_found, 'similarity_scores': similarity_scores})
    else:
        return jsonify({'error': 'Something Went Wrong!'}), 500

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000)
