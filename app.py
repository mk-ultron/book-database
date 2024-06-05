import streamlit as st
import sqlite3

# Function to execute a script from a .sql file
def execute_sql_script(conn, script_path):
    with open(script_path, 'r') as file:
        script = file.read()
    conn.executescript(script)

# Connect to SQLite database
conn = sqlite3.connect('books.db')
c = conn.cursor()

# Execute the SQL script to create tables and insert sample data
execute_sql_script(conn, 'setup.sql')

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
