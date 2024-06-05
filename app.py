import streamlit as st
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('books.db')
c = conn.cursor()

# Create tables
c.execute('CREATE TABLE IF NOT EXISTS authors (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL)')
c.execute('CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, author_id INTEGER, content BLOB, FOREIGN KEY (author_id) REFERENCES authors (id))')
c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, password TEXT NOT NULL)')
c.execute('CREATE TABLE IF NOT EXISTS reviews (id INTEGER PRIMARY KEY AUTOINCREMENT, book_id INTEGER, user_id INTEGER, rating INTEGER CHECK(rating >= 1 AND rating <= 5), review_text TEXT, FOREIGN KEY (book_id) REFERENCES books (id), FOREIGN KEY (user_id) REFERENCES users (id))')

# Insert sample data
-- Insert Authors
INSERT INTO authors (name) VALUES ('Author 1'), ('Author 2'), ('Author 3');

-- Insert Books
INSERT INTO books (title, author_id) VALUES ('Book 1', 1), ('Book 2', 2), ('Book 3', 3), ('Book 4', 1), ('Book 5', 2);

-- Insert Users
INSERT INTO users (username, password) VALUES ('user1', 'pass1'), ('user2', 'pass2');

-- Insert Reviews
INSERT INTO reviews (book_id, user_id, rating, review_text) VALUES
(1, 1, 5, 'Great book!'),
(2, 1, 4, 'Good read.'),
(3, 2, 3, 'Average.'),
(1, 2, 4, 'Enjoyable.'),
(2, 2, 5, 'Excellent!'),
(3, 1, 2, 'Not my type.'),
(4, 2, 4, 'Well written.'),
(5, 1, 5, 'Amazing book.'),
(4, 1, 3, 'Okay read.'),
(5, 2, 4, 'Good content.');


st.title('Online Book App')

# Display all books and their authors
st.header('Books and Authors')
books_authors = c.execute('SELECT books.title, authors.name FROM books JOIN authors ON books.author_id = authors.id').fetchall()
for book, author in books_authors:
    st.write(f'Book: {book}, Author: {author}')

# Retrieve all reviews for a specific book
st.header('Reviews for a Book')
book_id = st.number_input('Enter Book ID', min_value=1)
if st.button('Get Reviews'):
    reviews = c.execute('SELECT reviews.review_text, users.username FROM reviews JOIN users ON reviews.user_id = users.id WHERE reviews.book_id = ?', (book_id,)).fetchall()
    for review, user in reviews:
        st.write(f'User: {user}, Review: {review}')

# Retrieve books that have not been reviewed
st.header('Books Not Reviewed')
books_not_reviewed = c.execute('SELECT title FROM books WHERE id NOT IN (SELECT book_id FROM reviews)').fetchall()
for book in books_not_reviewed:
    st.write(f'Book: {book[0]}')

# Retrieve the average rating for each book
st.header('Average Rating for Each Book')
avg_ratings = c.execute('SELECT books.title, AVG(reviews.rating) as average_rating FROM books LEFT JOIN reviews ON books.id = reviews.book_id GROUP BY books.id').fetchall()
for book, rating in avg_ratings:
    st.write(f'Book: {book}, Average Rating: {rating}')

conn.close()
