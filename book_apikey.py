from flask import Flask, request, jsonify
#from flask_basicauth import BasicAuth
from functools import wraps

app = Flask(__name__)

# Basic authentication configuration
#app.config['BASIC_AUTH_USERNAME'] = 'username'
#app.config['BASIC_AUTH_PASSWORD'] = 'password'
#basic_auth = BasicAuth(app)

# Replace 'your_api_key' with your actual API key
API_KEY = 'your_api_key'

# API key authentication decorator
def require_api_key(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if request.headers.get('Api-Key') == API_KEY:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized"}), 401
    return decorated

# Sample data (in-memory database for simplicity)
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"},
    {"id": 3, "title": "Book 3", "author": "Author 3"}
]

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# Create (POST) operation
@app.route('/books', methods=['POST'])
#@basic_auth.required
@require_api_key
def create_book():
    data = request.get_json()

    new_book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data["author"]
    }

    books.append(new_book)
    return jsonify(new_book), 201

# Read (GET) operation - Get all books
@app.route('/books', methods=['GET'])
#@basic_auth.required
@require_api_key
def get_all_books():
    return jsonify({"books": books})

# Read (GET) operation - Get a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
#@basic_auth.required
@require_api_key
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Update (PUT) operation
@app.route('/books/<int:book_id>', methods=['PUT'])
#@basic_auth.required
@require_api_key
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        data = request.get_json()
        book.update(data)
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404

# Delete operation
@app.route('/books/<int:book_id>', methods=['DELETE'])
#@basic_auth.required
@require_api_key
def delete_book(book_id):
    global books
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted successfully"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

