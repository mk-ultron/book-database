import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BLOB, CheckConstraint, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import pyodbc
import pandas as pd

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Initialize connection.
@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["connections"]["books_db"]["server"]
        + ";DATABASE="
        + st.secrets["connections"]["books_db"]["database"]
        + ";UID="
        + st.secrets["connections"]["books_db"]["username"]
        + ";PWD="
        + st.secrets["connections"]["books_db"]["password"]
    )
    
conn = init_connection()

# Perform query.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

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

# Create an SQLAlchemy engine
engine = create_engine("mssql+pyodbc:///?odbc_connect=" + st.secrets["connections"]["books_db"]["url"])

# Create tables and insert sample data.
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

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
        Book(
            title='The Unlikely Hero',
            author_id=1,
            content="""
Once upon a time, in a small village nestled between towering mountains, there lived a humble mechanic named Kira. 
Kira was known throughout the village for her ability to fix anything, from broken pots to intricate machinery. 
Despite her talents, she yearned for adventure beyond the confines of her village.

One day, a mysterious traveler arrived, bearing news of a distant land in peril. The traveler spoke of a prophecy, 
foretelling that a hero from a humble background would rise to save the kingdom. Intrigued and feeling a sense of destiny, 
Kira decided to embark on this adventure.

Armed with her tools and unwavering determination, Kira journeyed across treacherous landscapes, facing numerous challenges. 
She encountered mythical creatures, formed alliances with unlikely companions, and discovered hidden strengths within herself.

As Kira's journey progressed, she uncovered a plot by an evil sorcerer to plunge the kingdom into eternal darkness. 
With the fate of the kingdom hanging in the balance, Kira confronted the sorcerer in an epic battle of wit and courage. 
Using her mechanical ingenuity, she managed to outsmart the sorcerer and thwart his plans.

Kira's bravery and resourcefulness not only saved the kingdom but also inspired others to find the hero within themselves. 
She returned to her village, forever changed by her journey, and was celebrated as the unlikely hero who rose from humble beginnings 
to achieve greatness.

And so, the tale of Kira, the mechanic turned savior, became a legend told for generations, reminding everyone that heroism 
can be found in the most unexpected places.
""".encode('utf-8'),  # Convert to bytes
            image_url='https://mk-ultron.github.io/ebook-reader/story-image1.png'
        ),
        Book(
            title='Echoes of the Future',
            author_id=2,
            content="""
In the sprawling metropolis of Neo-Tokyo, where neon lights illuminate the night sky, a young hacker named Jax navigated the shadows. 
Jax was renowned for his skills in breaching the most secure systems, but his latest mission was different. A hidden message 
from the future had been embedded in the city's network, warning of an impending disaster.

Determined to prevent the catastrophe, Jax embarked on a journey through the cybernetic underworld. He faced ruthless megacorporations 
and rogue AIs, uncovering secrets that revealed a grand conspiracy to control the city's future. With each step, Jax pieced together 
the puzzle, discovering that the disaster was orchestrated by a powerful entity seeking to rewrite history.

With time running out, Jax teamed up with a group of rebels who believed in a free and open future. Together, they launched a daring 
assault on the corporation's headquarters, navigating through layers of security and battling cybernetic enforcers.

In a climactic showdown, Jax confronted the mastermind behind the conspiracy. Using his unparalleled hacking abilities, he 
disrupted the entity's control and exposed the truth to the world. The city of Neo-Tokyo was saved from destruction, and its 
citizens were freed from the chains of a predetermined fate.

Jax's bravery and intellect became a beacon of hope, inspiring others to fight for their freedom and future. The echoes of his 
actions resonated through time, reminding all that the future is not set in stone.
""".encode('utf-8'),  # Convert to bytes
            image_url='https://mk-ultron.github.io/ebook-reader/story-image2.png'
        ),
        Book(
            title='The Clockwork Quest',
            author_id=3,
            content="""
In the steampunk city of Gearford, where clockwork machines and steam-powered inventions filled the streets, lived two young 
inventors named Elara and Gideon. The city was a marvel of engineering, but it was also a place of mystery and danger.

One day, a cryptic message arrived at their workshop, leading them to a hidden map that revealed the location of an ancient 
artifact known as the Clockwork Heart. This artifact was said to possess the power to bring any machine to life, and many sought 
it for their own purposes.

Determined to protect the Clockwork Heart from falling into the wrong hands, Elara and Gideon embarked on a perilous quest. 
They traveled through mechanical jungles, evaded cunning thieves, and solved intricate puzzles that tested their ingenuity and 
teamwork.

As they drew closer to their goal, they faced the ultimate challenge: a rival inventor who had been pursuing the artifact for 
his own gain. In a battle of wits and mechanical prowess, Elara and Gideon used their inventions to outsmart their opponent and 
secure the Clockwork Heart.

Returning to Gearford as heroes, they chose to keep the artifact safe and use its power to improve the lives of the city's 
inhabitants. Their adventure became a legend, inspiring future generations of inventors to pursue knowledge and innovation for 
the greater good.
""".encode('utf-8'),  # Convert to bytes
            image_url='https://mk-ultron.github.io/ebook-reader/story-image3.png'
        ),
        Book(
            title='The Hidden Underworld',
            author_id=4,
            content="""
Beneath the bustling streets of New Avalon, a hidden world of magic and mystery thrived. Lila Blake, a skilled detective with 
a knack for uncovering secrets, was well-acquainted with this underworld. Her latest case, however, would take her deeper than 
ever before.

A series of disappearances had plagued the city, with each victim leaving behind only a faint trace of magical residue. Lila's 
investigation led her to an ancient artifact, the Shadow Amulet, which had the power to manipulate the very fabric of reality.

As Lila delved deeper, she uncovered a dark plot by a rogue sorcerer to use the Amulet's power to merge the underworld with the 
surface, creating a realm where he would reign supreme. With the help of a reformed thief and a scholar of ancient lore, Lila 
raced against time to stop the sorcerer.

Navigating through enchanted forests, deciphering ancient runes, and facing magical traps, Lila and her companions pressed on. 
In a final confrontation within the heart of the underworld, Lila's quick thinking and resourcefulness allowed her to reclaim 
the Amulet and defeat the sorcerer.

The city of New Avalon was saved, and the barrier between the worlds was restored. Lila's bravery and determination earned her 
renown, and the tales of her exploits in the hidden underworld became a source of inspiration for all who heard them.
""".encode('utf-8'),  # Convert to bytes
            image_url='https://mk-ultron.github.io/ebook-reader/story-image4.png'
        ),
        Book(
            title='The Quest for the Crystal',
            author_id=5,
            content="""
In the mystical realm of Eldoria, where magic and wonder were woven into the very fabric of reality, a dire prophecy foretold 
the return of darkness unless a group of heroes could retrieve the legendary Crystal of Light. Among these heroes was Thorne 
Brightblade, a courageous warrior with a heart of gold.

Joined by a diverse group of adventurers—a skilled mage, a stealthy rogue, and a wise druid—Thorne set out on an epic journey. 
They traversed enchanted forests, scaled treacherous mountains, and delved into ancient ruins, each step bringing them closer 
to their goal.

Along the way, they faced formidable foes and forged unbreakable bonds of friendship. They discovered that the Crystal of Light 
was guarded by a powerful dragon, a creature of both awe and terror. In a climactic battle, Thorne and his companions combined 
their strengths and knowledge to outwit the dragon and claim the Crystal.

Returning to Eldoria, they used the Crystal's power to dispel the encroaching darkness, restoring peace and balance to the realm. 
Their quest became the stuff of legends, a testament to the power of unity, courage, and hope.

Thorne's name, along with those of his companions, was etched into the annals of history, reminding all who heard their story 
that even in the darkest times, the light of heroism can shine through.
""".encode('utf-8'),  # Convert to bytes
            image_url='https://mk-ultron.github.io/ebook-reader/story-image5.png'
        )
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
        Review(book_id=5, user_id=9, rating=5, review_text="An epic quest filled with danger, magic, and camaraderie. The team’s journey to find the Crystal of Light is legendary!"),
        Review(book_id=5, user_id=10, rating=4, review_text="A fantastic fantasy adventure that will transport you to the realm of Eldoria. The characters and plot are truly enchanting.")
    ]
    session.add_all(reviews)
    session.commit()

# Streamlit app title
st.title('AI Fast Fiction Database')

# Display all books and their authors
st.header('Current Fiction')
books_authors_ratings = run_query("""
    SELECT b.id, b.title, a.name, b.image_url, AVG(r.rating)
    FROM books b
    JOIN authors a ON b.author_id = a.id
    LEFT JOIN reviews r ON b.id = r.book_id
    GROUP BY b.id, b.title, a.name, b.image_url
""")

# Display each book with its details and reviews
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
            reviews = run_query(f"""
                SELECT r.review_text, u.username
                FROM reviews r
                JOIN users u ON r.user_id = u.id
                WHERE r.book_id = {book_id}
            """)
            with col3:
                for review, user in reviews:
                    st.markdown(f"**{user}**")
                    st.markdown(f"{review}")
        if st.button('Show Full Text', key=f"text_button_{book_id}"):
            book_content = run_query(f"SELECT content FROM books WHERE id = {book_id}")
            if book_content and book_content[0]:
                st.text_area(f"Full Text of {book}", book_content[0][0].decode('utf-8'))

if st.button('Show Books Without Reviews'):
    books_not_reviewed = run_query("""
        SELECT b.title, b.image_url, a.name
        FROM books b
        JOIN authors a ON b.author_id = a.id
        LEFT JOIN reviews r ON b.id = r.book_id
        WHERE r.id IS NULL
    """)
    st.header('Books Without Reviews')
    for book, image_url, author in books_not_reviewed:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(image_url)  # Display image from URL
        with col2:
            st.markdown(f"### {book}")
            st.markdown(f"Author: {author}")

# Add a section to view raw data from the database
st.header('View Raw Data')

# Fetch and display data from the authors table
st.subheader('Authors')
authors_data = run_query("SELECT id, name FROM authors")
authors_df = pd.DataFrame(authors_data, columns=['ID', 'Name'])
st.dataframe(authors_df)

# Fetch and display data from the books table
st.subheader('Books')
books_data = run_query("SELECT id, title, author_id, image_url FROM books")
books_df = pd.DataFrame(books_data, columns=['ID', 'Title', 'Author ID', 'Image URL'])
st.dataframe(books_df)

# Fetch and display data from the users table
st.subheader('Users')
users_data = run_query("SELECT id, username FROM users")
users_df = pd.DataFrame(users_data, columns=['ID', 'Username'])
st.dataframe(users_df)

# Fetch and display data from the reviews table
st.subheader('Reviews')
reviews_data = run_query("SELECT id, book_id, user_id, rating, review_text FROM reviews")
reviews_df = pd.DataFrame(reviews_data, columns=['ID', 'Book ID', 'User ID', 'Rating', 'Review Text'])
st.dataframe(reviews_df

# Close the session to the database
session.close()
