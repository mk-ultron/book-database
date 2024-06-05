import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BLOB, CheckConstraint, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Create the SQL connection to books_db as specified in your secrets file.
database_url = st.secrets["connections"]["books_db"]["url"]
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    content = Column(BLOB)
    author = relationship('Author', back_populates='books')

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    review_text = Column(String)
    book = relationship('Book', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

Author.books = relationship('Book', order_by=Book.id, back_populates='author')
Book.reviews = relationship('Review', order_by=Review.id, back_populates='book')
User.reviews = relationship('Review', order_by=Review.id, back_populates='user')

# Create tables and insert sample data
Base.metadata.create_all(engine)

# Insert sample data if not already present
if not session.query(Author).first():
    authors = [Author(name='Author 1'), Author(name='Author 2'), Author(name='Author 3')]
    session.add_all(authors)
    session.commit()

if not session.query(Book).first():
    books = [
        Book(title='Book 1', author_id=1),
        Book(title='Book 2', author_id=2),
        Book(title='Book 3', author_id=3),
        Book(title='Book 4', author_id=1),
        Book(title='Book 5', author_id=2)
    ]
    session.add_all(books)
    session.commit()

if not session.query(User).first():
    users = [User(username='user1', password='pass1'), User(username='user2', password='pass2')]
    session.add_all(users)
    session.commit()

if not session.query(Review).first():
    reviews = [
        Review(book_id=1, user_id=1, rating=5, review_text='Great book!'),
        Review(book_id=2, user_id=1, rating=4, review_text='Good read.'),
        Review(book_id=3, user_id=2, rating=3, review_text='Average.'),
        Review(book_id=1, user_id=2, rating=4, review_text='Enjoyable.'),
        Review(book_id=2, user_id=2, rating=5, review_text='Excellent!'),
        Review(book_id=3, user_id=1, rating=2, review_text='Not my type.'),
        Review(book_id=4, user_id=2, rating=4, review_text='Well written.'),
        Review(book_id=5, user_id=1, rating=5, review_text='Amazing book.'),
        Review(book_id=4, user_id=1, rating=3, review_text='Okay read.'),
        Review(book_id=5, user_id=2, rating=4, review_text='Good content.')
    ]
    session.add_all(reviews)
    session.commit()

st.title('Online Book App')

# Display all books and their authors
st.header('Books and Authors')
books_authors = session.query(Book.title, Author.name).join(Author).all()
for book, author in books_authors:
    st.write(f'Book: {book}, Author: {author}')

# Retrieve all reviews for a specific book
st.header('Reviews for a Book')
book_id = st.number_input('Enter Book ID', min_value=1)
if st.button('Get Reviews'):
    reviews = session.query(Review.review_text, User.username).join(User).filter(Review.book_id == book_id).all()
    for review, user in reviews:
        st.write(f'User: {user}, Review: {review}')

# Retrieve books that have not been reviewed
st.header('Books Not Reviewed')
books_not_reviewed = session.query(Book.title).outerjoin(Review).filter(Review.id == None).all()
for book in books_not_reviewed:
    st.write(f'Book: {book[0]}')

# Retrieve the average rating for each book
st.header('Average Rating for Each Book')
avg_ratings = session.query(Book.title, func.avg(Review.rating)).join(Review).group_by(Book.id).all()
for book, rating in avg_ratings:
    st.write(f'Book: {book}, Average Rating: {rating}')

session.close()
