import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BLOB, CheckConstraint, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import pandas as pd

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
    content = Column(BLOB)  # Store the full text of the book
    image_url = Column(String)  # Store the image URL instead of BLOB
    author = relationship('Author', back_populates='books')

# Define the User model/table.
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)

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

# Create tables and insert sample data.
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
        Book(title='The Unlikely Hero', author_id=1, content=b'The galaxy was at war. Starfleets clashed in the cold void, planets burned, and alliances crumbled. Amidst this chaos, Kira, a lowly mechanic on the barren moon of Kestris, found herself thrust into the heart of the conflict. She had always believed her life would be spent repairing starships and dreaming of adventure, but fate had other plans.
One fateful day, while scavenging for parts, Kira stumbled upon a crashed escape pod. Inside was a gravely injured alien who identified himself as Prince Thallan, heir to the Throne of Arion, a planet key to the balance of power in the galaxy. The prince carried a message of a greater threat—an ancient, malevolent force from beyond the stars, known as the Voidbringers, poised to conquer and consume all in their path.
With his dying breath, Prince Thallan entrusted Kira with a data crystal containing vital information that could unite the warring factions against the Voidbringers. Kira, never one to shirk from a challenge, vowed to honor the prince's last wish. She repaired a derelict starfighter, took the crystal, and embarked on a perilous journey.
Her path was fraught with danger—she faced hostile patrols, treacherous smugglers, and the ever-looming threat of the Voidbringers. Along the way, she forged unlikely alliances with rebels, outlaws, and soldiers from enemy planets. Kira's courage and determination inspired those she met, and her mission quickly became a beacon of hope.
In the climactic battle, as the Voidbringers descended upon the galaxy, Kira's ragtag fleet, now united, launched a desperate defense. With the help of the data crystal, they discovered the Voidbringers' weakness and struck a decisive blow. The galaxy, though scarred by war, was saved.
Kira, the mechanic turned hero, had done the impossible. She had united the galaxy and defeated the greatest threat it had ever faced. The war ended, and peace, though fragile, began to bloom. Kira returned to Kestris, but her name would forever be remembered among the stars.', image_url='https://mk-ultron.github.io/ebook-reader/story-image1.png'),
        Book(title='Echoes of the Future', author_id=2, content=b'Full text of Echoes of the Future...', image_url='https://mk-ultron.github.io/ebook-reader/story-image2.png'),
        Book(title='The Clockwork Quest', author_id=3, content=b'Full text of The Clockwork Quest...', image_url='https://mk-ultron.github.io/ebook-reader/story-image3.png'),
        Book(title='The Hidden Underworld', author_id=4, content=b'Full text of The Hidden Underworld...', image_url='https://mk-ultron.github.io/ebook-reader/story-image4.png'),
        Book(title='The Quest for the Crystal', author_id=5, content=b'Full text of The Quest for the Crystal...', image_url='https://mk-ultron.github.io/ebook-reader/story-image5.png')
    ]
    session.add_all(books)
    session.commit()

# Insert sample data if not already present in the users table.
if not session.query(User).first():
    users = [User(username='GalacticGeek'), User(username='SpaceCadet99'), 
             User(username='CyberPunk42'), User(username='MatrixMaster'), 
             User(username='SteampunkSally'), User(username='AirshipAdventurer'),
             User(username='MagicMaven'), User(username='DetectiveDynamo'),
             User(username='FantasyFanatic'), User(username='KnightOfLore')]
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
        Review(book_id=4, user_id=7, rating=5, review_text="Lila Blake’s journey through New Avalon’s magical underworld is spellbinding. A perfect blend of mystery and fantasy!"),
        Review(book_id=4, user_id=8, rating=4, review_text="A thrilling detective story with a magical twist. Lila’s quest to save New Avalon is a page-turner."),
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

# Display each book with its details and reviews
for book_id, book, author, image_url, avg_rating in books_authors_ratings:
    col1, col2, col3 = st.columns([1, 3, 3])
    with col1:
        st.image(image_url)  # Display image from URL
    with col2:
        st.markdown(f"### {book}")
        st.markdown(f"Author: {author}")
        st.markdown(f"Average Rating: {avg_rating:.2f}")
        if st.button('Show Reviews', key=f"button_{book_id}"):
            col3.empty()
            reviews = session.query(Review.review_text, User.username).join(User).filter(Review.book_id == book_id).all()
            with col3:
                for review, user in reviews:
                    st.markdown(f"**{user}**")
                    st.markdown(f"{review}")
        if st.button('Show Full Text', key=f"text_button_{book_id}"):
            book_content = session.query(Book.content).filter(Book.id == book_id).first()
            if book_content and book_content[0]:
                st.text_area(f"Full Text of {book}", book_content[0].decode('utf-8'))

# Add a section to view raw data from the database
st.header('View Raw Data')

# Fetch and display data from the authors table
st.subheader('Authors')
authors_data = session.query(Author).all()
authors_df = pd.DataFrame([(author.id, author.name) for author in authors_data], columns=['ID', 'Name'])
st.dataframe(authors_df)

# Fetch and display data from the books table
st.subheader('Books')
books_data = session.query(Book).all()
books_df = pd.DataFrame([(book.id, book.title, book.author_id, book.image_url) for book in books_data], columns=['ID', 'Title', 'Author ID', 'Image URL'])
st.dataframe(books_df)

# Fetch and display data from the users table
st.subheader('Users')
users_data = session.query(User).all()
users_df = pd.DataFrame([(user.id, user.username) for user in users_data], columns=['ID', 'Username'])
st.dataframe(users_df)

# Fetch and display data from the reviews table
st.subheader('Reviews')
reviews_data = session.query(Review).all()
reviews_df = pd.DataFrame([(review.id, review.book_id, review.user_id, review.rating, review.review_text) for review in reviews_data], columns=['ID', 'Book ID', 'User ID', 'Rating', 'Review Text'])
st.dataframe(reviews_df)

# Close the session to the database
session.close()
