from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import re
import uvicorn

app = FastAPI()

# Library books dataset
books = [
    {"id": "01", "title": "The Silent Patient", "author": "Alex Michaelides", "in_shelf": True},
    {"id": "02", "title": "Atomic Habits", "author": "James Clear", "in_shelf": False},
    {"id": "03", "title": "Educated", "author": "Tara Westover", "in_shelf": True},
    {"id": "04", "title": "Where the Crawdads Sing", "author": "Delia Owens", "in_shelf": False},
    {"id": "05", "title": "The Midnight Library", "author": "Matt Haig", "in_shelf": True},
    {"id": "06", "title": "Becoming", "author": "Michelle Obama", "in_shelf": True},
    {"id": "07", "title": "The Four Agreements", "author": "Don Miguel Ruiz", "in_shelf": False},
    {"id": "08", "title": "Sapiens", "author": "Yuval Noah Harari", "in_shelf": True},
    {"id": "09", "title": "The Alchemist", "author": "Paulo Coelho", "in_shelf": False},
    {"id": "10", "title": "The Power of Now", "author": "Eckhart Tolle", "in_shelf": True},
    {"id": "11", "title": "Journey to Peace 1", "author": "Lama Yeshe", "in_shelf": True},
    {"id": "12", "title": "Mindfulness Practice 2", "author": "Thich Nhat Hanh", "in_shelf": False},
    {"id": "13", "title": "Deep Work 3", "author": "Cal Newport", "in_shelf": True},
    {"id": "14", "title": "Atomic Habits 4", "author": "James Clear", "in_shelf": False},
    {"id": "15", "title": "The 5 AM Club 101", "author": "Robin Sharma", "in_shelf": True}
]

# Users dataset
users = [
    {"user_id": 1, "name": "Alice Johnson", "email": "alice.johnson@example.com", "phone": "+234900567890",
        "membership_date": "2022-01-15", "active": True, "borrowed_books_count": 3},
    {"user_id": 2, "name": "Brian Smith", "email": "brian.smith@example.com", "phone": "+234810567891",
        "membership_date": "2021-09-10", "active": True, "borrowed_books_count": 1},
    {"user_id": 3, "name": "Clara Lee", "email": "clara.lee@example.com", "phone": "+234901567892",
        "membership_date": "2023-04-22", "active": False, "borrowed_books_count": 0},
    {"user_id": 4, "name": "David Kim", "email": "david.kim@example.com", "phone": "+234701567893",
        "membership_date": "2020-11-05", "active": True, "borrowed_books_count": 4},
    {"user_id": 5, "name": "Ella Martinez", "email": "ella.martinez@example.com", "phone": "+234809567894",
        "membership_date": "2022-06-30", "active": True, "borrowed_books_count": 2}
]

# Borrow books dataset
borrowed_books = [
    {"borrow_id": 101, "user_name": "Alice Johnson", "book_id": "03", "borrow_date": "2024-12-01",
        "due_date": "2024-12-15", "return_date": "2024-12-14"},
    {"borrow_id": 102, "user_name": "Brian Smith", "book_id": "07", "borrow_date": "2025-01-10",
        "due_date": "2025-01-24", "return_date": "2025-01-30"},
    {"borrow_id": 103, "user_name": "Ella Martinez", "book_id": "01", "borrow_date": "2025-02-01",
        "due_date": "2025-02-15", "return_date": None},
    {"borrow_id": 104, "user_name": "David Kim", "book_id": "03", "borrow_date": "2025-03-01",
        "due_date": "2025-03-15", "return_date": "2025-03-12"}
]



### API FUNCTIONS

#SERVER ROUTES DISPLAYING DATA
# The root server page
from fastapi.responses import HTMLResponse
from fastapi import FastAPI

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h2 style="text-align: center;">📚 Oladoyin's E-Library API</h2>
    <h3 style="text-align: center;">Available Endpoints:</h3>
    <ul style="line-height: 1.8; font-size: 16px; width: 60%; margin: auto;">
        <li><b>Root:</b> <a href="/">http://127.0.0.1:8000/</a></li>
        <li><b>Interactive Docs:</b> <a href="/docs">http://127.0.0.1:8000/docs</a></li>
        <li><b>All Books:</b> <a href="/books">http://127.0.0.1:8000/books</a></li>
        <li><b>Get Book by Title:</b> <code>/books/title/book title</code></li>
        <li><b>Get Book by Author:</b> <code>/books/author/author's full name</code></li>
        <li><b>Get Books with Prime ID:</b> <a href="/books/primeid">/books/primeid</a></li>
        <li><b>Get Books with Prime Suffix in Title:</b> <a href="/books/primesuffix">/books/primesuffix</a></li>
        <li><b>Add Book:</b> <a href="http://127.0.0.1:8000/docs#/default/add_book_books_add_post">POST http://127.0.0.1:8000/books/add</a> – accepts: {"id": id, "title": title, "author": author}</li>
        <li><b>Delete Book:</b> <a href="http://127.0.0.1:8000/docs#/default/delete_book_books_delete_post">POST http://127.0.0.1:8000/books/delete</a> – accepts: {"id": id, "title": title, "author": author}</li>
    </ul>
    """


# The server route showing books data
@app.get("/books/", response_class=HTMLResponse)
def get_books():
    table = """<h2 style="text-align: center;">Books</h2>
    <table border="1" style="border-collapse: collapse; width: 45%; margin: 0 auto;">
        <tr>
            <th style="text-align: left; padding: 8px;">ID</th>
            <th style="text-align: left; padding: 8px;">Title</th>
            <th style="text-align: left; padding: 8px;">Author</th>
            <th style="text-align: left; padding: 8px;">Shelf Status</th>
        </tr>
    """

    for book in books:
        table += f"<tr><td>{book['id']}</td><td>{book['title']}</td><td>{book['author']}</td><td>{book['in_shelf']}</td></tr>"

    table += "</table>"
    return table


# The server route showing user data
@app.get("/users/", response_class=HTMLResponse)
def get_users():
    table = """<h2 style="text-align: center;">Users</h2>
    <table border="1" style="border-collapse: collapse; width: 75%; margin: 0 auto;">
        <tr>
            <th style="text-align: left; padding: 8px;">User ID</th>
            <th style="text-align: left; padding: 8px;">Name</th>
            <th style="text-align: left; padding: 8px;">Email</th>
            <th style="text-align: left; padding: 8px;">Phone Number</th>
            <th style="text-align: left; padding: 8px;">Membership Date</th>
            <th style="text-align: left; padding: 8px;">Active Status</th>
            <th style="text-align: left; padding: 8px;">No. of Borrowed Books</th>
        </tr>
    """

    for user in users:
        table += f"<tr><td>{user['user_id']}</td><td>{user['name']}</td><td>{user['email']}</td><td>{user['phone']}</td><td>{user['membership_date']}</td><td>{user['active']}</td><td>{user['borrowed_books_count']}</td></tr>"

    table += "</table>"
    return table


# The server route showing borrowed books' data
@app.get("/borrowed/", response_class=HTMLResponse)
def get_borrowed_books():
    table = """<h2 style="text-align: center;">Borrowed Books</h2>
    <table border="1" style="border-collapse: collapse; width: 75%; margin: 0 auto;">
        <tr>
            <th style="text-align: left; padding: 8px;">Borrow ID</th>
            <th style="text-align: left; padding: 8px;">User Name</th>
            <th style="text-align: left; padding: 8px;">Book ID</th>
            <th style="text-align: left; padding: 8px;">Borrow Date</th>
            <th style="text-align: left; padding: 8px;">Due Date</th>
            <th style="text-align: left; padding: 8px;">Return Date</th>
        </tr>
    """

    for borrowed_book in borrowed_books:
        table += f"<tr><td>{borrowed_book['borrow_id']}</td><td>{borrowed_book['user_name']}</td><td>{borrowed_book['book_id']}</td><td>{borrowed_book['borrow_date']}</td><td>{borrowed_book['due_date']}</td><td>{borrowed_book['return_date']}</td></tr>"

    table += "</table>"
    return table



## SERVER GET AND POST ROUTE FUNCTIONS

# 1. Route to Get book by title
@app.get("/books/title/{book_title}")
def get_book_by_title(book_title: str):
    book_list = []
    for book in books:
        if book['title'].lower() == book_title.lower(): 
            book_list.append(book)
    return book_list if len(book_list) > 0 else "Book with that title not found in library"


# 2. Route to Get book by author
@app.get("/books/author/{book_author}")
def get_book_by_author(book_author: str):
    book_list = []
    for book in books:
        book_list.append(book) if book['author'].lower() == book_author.lower() else None            
    return book_list if len(book_list) > 0 else "Book by that author not found in library"


# 3. Route to Get books with prime IDs

# Function to define conditions for prime numbers
def is_prime(n):
    # If less than 2, not prime
    if n <= 1:
        return False 
    # If 2, prime
    if n == 2:
        return True 
    # If even and not 2, not prime
    if n % 2 == 0:
        return False 
    # If odd and not divisible by odd numbers up to sqrt(number), prime
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False #
    return True

# Request-Response function 
@app.get("/books/primeid")
def get_books_with_primeID():
    book_list = []
    for book in books:
        book_list.append(book) if is_prime(int(book['id'])) else None            
    return book_list


# 4. Route to Get books with prime title suffix
@app.get("/books/primesuffix")
def get_books_with_primeSuffix():
    book_list = []
    for book in books:
        match = re.search(r"(\d+)$", book['title'])
        if match:
            number = int(match.group())
            book_list.append(book) if is_prime(number) else None
    return book_list


# 5. Route to Add book to books database
@app.post("/books/add")
def add_book(new_book: dict):
    book_id = int(new_book['id'])
    book_title = new_book['title'].lower()
    book_author = new_book['author'].lower()

    for book in books:
        if int(book['id']) == book_id:
            last_id = max(int(book["id"]) for book in books)
            return f"Book ID already used. Use {last_id + 1} instead!"
    for book in books:
        if (book['title'].lower() == book_title) and (book['author'].lower() == book_author):
            return f"Book already in library records {book}"

    books.append({'id': book_id, 'title': book_title, 'author': book_author, "in_shelf": True})
    return f"{book_title.capitalize()} by {book_author.title()} added to library!"


# 6. Route to Delete book from books database
@app.post("/books/delete")
def delete_book(new_book: dict):
    book_id = int(new_book['id'])
    book_title = new_book['title'].lower()
    book_author = new_book['author'].lower()

    for book in books:
        if int(book["id"]) == book_id and book["title"].lower() == book_title and book["author"].lower() == book_author:
            if book["in_shelf"]:
                books.remove(book)
                return f"{book_title.title()} by {book_author.title()} removed from library records."
            else:
                return "Book is not on the shelf. Cannot delete until it is returned."
    
    return "Incorrect book records. Delete not completed."