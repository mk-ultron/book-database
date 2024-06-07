import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BLOB, CheckConstraint, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Create the SQL connection to books_db as specified in your secrets file.
database_url = st.secrets["connections"]["books_db"]["url"]
engine = create_engine(database_url)
Session = sessionmaker(bind=engine)
session = Session()

# Base class for declarative class definitions.
Base = declarative_base()

# Define the Author model/table.
class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

# Define the Book model/table.
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    content = Column(BLOB)
    image_url = Column(String)  # Store the image URL instead of BLOB
    author = relationship('Author', back_populates='books')

# Define the User model/table.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

# Define the Review model/table.
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    review_text = Column(String)
    book = relationship('Book', back_populates='reviews')
    user = relationship('User', back_populates='reviews')

# Establish relationships between models.
Author.books = relationship('Book', order_by=Book.id, back_populates='author')
Book.reviews = relationship('Review', order_by=Review.id, back_populates='book')
User.reviews = relationship('Review', order_by=Review.id, back_populates='user')

# Create tables and insert sample data
Base.metadata.create_all(engine)

# Insert sample data if not already present in the authors table.
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

# Insert sample data if not already present in the books table.
if not session.query(Book).first():
    books = [
        Book(title='The Unlikely Hero', author_id=1, image_url='https://mk-ultron.github.io/ebook-reader/story-image1.png'),
        Book(title='Echoes of the Future', author_id=2, image_url='https://mk-ultron.github.io/ebook-reader/story-image2.png'),
        Book(title='The Clockwork Quest', author_id=3, image_url='https://mk-ultron.github.io/ebook-reader/story-image3.png'),
        Book(title='The Hidden Underworld', author_id=4, image_url='https://mk-ultron.github.io/ebook-reader/story-image4.png'),
        Book(title='The Quest for the Crystal', author_id=5, image_url='https://mk-ultron.github.io/ebook-reader/story-image5.png')
    ]
    session.add_all(books)
    session.commit()

# Insert sample data if not already present in the users table.
if not session.query(User).first():
    users = [User(username='GalacticGeek', password='pass1'), User(username='SpaceCadet99', password='pass2'), 
             User(username='CyberPunk42', password='pass3'), User(username='MatrixMaster', password='pass4'), 
             User(username='SteampunkSally', password='pass5'), User(username='AirshipAdventurer', password='pass6'),
             User(username='MagicMaven', password='pass7'), User(username='DetectiveDynamo', password='pass8'),
             User(username='FantasyFanatic', password='pass9'), User(username='KnightOfLore', password='pass10')]
    session.add_all(users)
    session.commit()
    
# Insert sample data if not already present in the reviews table.
if not session.query(Review).first():
    reviews = [
        Review(book_id=1, user_id=1, rating=5, review_text="Kira’s journey from a humble mechanic to a galactic savior is nothing short of inspirational. The plot twists kept me on the edge of my seat!"),
        Review(book_id=1, user_id=2, rating=4, review_text="A thrilling space opera that combines heart and heroism. Kira is the hero we all need!"),
        Review(book_id=2, user_id=3, rating=5, review_text="Jax’s battle against megacorporations is a gripping cyber adventure. The neon-lit streets of Neo-Tokyo are vividly portrayed!"),
        Review(book_id=2, user_id=4, rating=4, review_text="An exhilarating dive into a digital dystopia. Jax is the perfect rogue hacker hero for this thrilling tale."),
        Review(book_id=3, user_id=5, rating=5, review_text="Elara and Gideon’s quest is filled with clockwork marvels and daring escapades. Gearford is a city that sparks the imagination!"),
        Review(book_id=3, user_id=6, rating=4, review_text="A captivating steampunk adventure with brilliant inventions and a race against time. Elara is a fantastic protagonist."),
        Review(book_id=5, user_id=9, rating=5, review_text="An epic quest filled with danger, magic, and camaraderie. The team’s journey to find the Crystal of Light is legendary!"),
        Review(book_id=5, user_id=10, rating=4, review_text="A fantastic fantasy adventure that will transport you to the realm of Eldoria. The characters and plot are truly enchanting.")
    ]
    session.add_all(reviews)
    session.commit()
    
# Streamlit app title
st.title('AI Fast Fiction Database')

# Display all books and their authors
st.header('Current Fiction')
books_authors_ratings = session.query(Book.id, Book.title, Author.name, Book.image_url, func.avg(Review.rating)).join(Author).outerjoin(Review).group_by(Book.id).all()

for book_id, book, author, image_url, avg_rating in books_authors_ratings:
    col1, col2, col3 = st.columns([1, 3, 3])
    with col1:
        st.image(image_url)  # Display image from URL
    with col2:
        st.markdown(f"### {book}")
        st.markdown(f"Author: {author}")
        if avg_rating is not None:
            st.markdown(f"Average Rating: {avg_rating:.2f}")
        else:
            st.markdown("Average Rating: No ratings yet")
        if st.button('Show Reviews', key=f"button_{book_id}"):
            reviews = session.query(Review.review_text, User.username).join(User).filter(Review.book_id == book_id).all()
            with col3:
                for review, user in reviews:
                    st.markdown(f"**{user}**")
                    st.markdown(f"{review}")

if st.button('Show Books Without Reviews'):
    books_not_reviewed = session.query(Book.title, Book.image_url, Author.name).join(Author).outerjoin(Review).filter(Review.id == None).all()
    st.header('Books Without Reviews')
    for book, image_url, author in books_not_reviewed:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(image_url)  # Display image from URL
        with col2:
            st.markdown(f"### {book}")
            st.markdown(f"Author: {author}")

session.close()
