## AI Fast Fiction Database

This project is a Streamlit application that showcases a fictional book database. It uses SQLAlchemy for database interactions and stores book data, authors, users, and reviews. The app displays books along with their authors and average ratings, and allows users to view detailed reviews.

## Features

- Display a list of books along with their authors and average ratings.
- View detailed reviews for each book.
- Store and manage data for books, authors, users, and reviews using SQLAlchemy.

## Requirements

- Python 3.7 or higher
- Streamlit
- SQLAlchemy

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/mk-ultron/book-database.git
   cd book-database
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `secrets.toml` file in the `.streamlit` directory with your database URL:

   ```toml
   [connections.books_db]
   url = "sqlite:///books.db"
   ```

5. Run the application:

   ```bash
   streamlit run app.py
   ```

## Project Structure

- `app.py`: The main Streamlit application file.
- `requirements.txt`: List of required Python packages.
- `.streamlit/secrets.toml`: Configuration file for database connection (not included in the repository, needs to be created by the user).

## Database Schema

The database consists of four tables:

1. `authors`: Stores author information.
2. `books`: Stores book information and links to the author.
3. `users`: Stores user information.
4. `reviews`: Stores reviews, including ratings and review text, linking books and users.

## Example Data

The application includes ai-generated data for authors, books, users, and reviews. This data is inserted into the database if it does not already exist.

## Usage

Once the application is running, you can interact with it through the web interface. The homepage displays a list of books with their authors and average ratings. You can click the "Show Reviews" button to view detailed reviews for each book.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes or improvements.
