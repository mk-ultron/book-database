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
    authors = [
        Author(name='Aria Starwind'), 
        Author(name='Ryker Blackwood'), 
        Author(name='Ivy Gearheart'),
        Author(name='Luna Nightshade'),
        Author(name='Thorne Brightblade')
    ]
    session.add_all(authors)
    session.commit()

if not session.query(Book).first():
    books = [
        Book(title='The Unlikely Hero', author_id=1),
        Book(title='Echoes of the Future', author_id=2),
        Book(title='The Clockwork Quest', author_id=3),
        Book(title='The Hidden Underworld', author_id=4),
        Book(title='The Quest for the Crystal', author_id=5)
    ]
    session.add_all(books)
    session.commit()

if not session.query(User).first():
    users = [User(username='user1', password='pass1'), User(username='user2', password='pass2')]
    session.add_all(users)
    session.commit()

if not session.query(Review).first():
    reviews = [
        Review(book_id=1, user_id=1, rating=5, review_text="GalacticGeek: Kira’s journey from a humble mechanic to a galactic savior is nothing short of inspirational. The plot twists kept me on the edge of my seat!"),
        Review(book_id=1, user_id=2, rating=4, review_text="SpaceCadet99: A thrilling space opera that combines heart and heroism. Kira is the hero we all need!"),
        Review(book_id=2, user_id=1, rating=5, review_text="CyberPunk42: Jax’s battle against megacorporations is a gripping cyber adventure. The neon-lit streets of Neo-Tokyo are vividly portrayed!"),
        Review(book_id=2, user_id=2, rating=4, review_text="MatrixMaster: An exhilarating dive into a digital dystopia. Jax is the perfect rogue hacker hero for this thrilling tale."),
        Review(book_id=3, user_id=1, rating=5, review_text="SteampunkSally: Elara and Gideon’s quest is filled with clockwork marvels and daring escapades. Gearford is a city that sparks the imagination!"),
        Review(book_id=3, user_id=2, rating=4, review_text="AirshipAdventurer: A captivating steampunk adventure with brilliant inventions and a race against time. Elara is a fantastic protagonist."),
        Review(book_id=4, user_id=1, rating=5, review_text="MagicMaven: Lila Blake’s journey through New Avalon’s magical underworld is spellbinding. A perfect blend of mystery and fantasy!"),
        Review(book_id=4, user_id=2, rating=4, review_text="DetectiveDynamo: A thrilling detective story with a magical twist. Lila’s quest to save New Avalon is a page-turner."),
        Review(book_id=5, user_id=1, rating=5, review_text="FantasyFanatic: An epic quest filled with danger, magic, and camaraderie. The team’s journey to find the Crystal of Light is legendary!"),
        Review(book_id=5, user_id=2, rating=4, review_text="KnightOfLore: A fantastic fantasy adventure that will transport you to the realm of Eldoria. The characters and plot are truly enchanting.")
    ]
    session.add_all(reviews)
    session.commit()

st.title('AI Fast Fiction Database')

# Display all books and their authors
st.header('Current Fiction')
books_authors_ratings = session.query(Book.title, Author.name, func.avg(Review.rating)).join(Author).outerjoin(Review).group_by(Book.id).all()
for book, author, avg_rating in books_authors_ratings:
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("https://via.placeholder.com/150")  # Placeholder image, replace with actual book cover URL
    with col2:
        st.markdown(f"### {book}")
        st.markdown(f"Author: {author}")
        st.markdown(f"Average Rating: {avg_rating:.2f}")

# Retrieve all reviews for a specific book
st.header('Reviews for a Book')
book_id = st.number_input('Enter Book ID', min_value=1)
if st.button('Get Reviews'):
    reviews = session.query(Review.review_text, User.username).join(User).filter(Review.book_id == book_id).all()
    for review, user in reviews:
        st.markdown(f"**{user}**")
        st.markdown(f"{review}")

# Retrieve books that have not been reviewed
st.header('Books Not Reviewed')
books_not_reviewed = session.query(Book.title).outerjoin(Review).filter(Review.id == None).all()
for book in books_not_reviewed:
    st.markdown(f"{book[0]}")

session.close()
