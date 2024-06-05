-- setup.sql

-- Authors Table
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Books Table
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author_id INTEGER,
    content BLOB,
    FOREIGN KEY (author_id) REFERENCES authors (id)
);

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

-- Reviews Table
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER,
    user_id INTEGER,
    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
    review_text TEXT,
    FOREIGN KEY (book_id) REFERENCES books (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Insert Authors
INSERT INTO authors (name) VALUES ('Author 1'), ('Author 2'), ('Author 3');

-- Insert Books
INSERT INTO books (title, author_id, content) VALUES 
('Book 1', 1, null), 
('Book 2', 2, null), 
('Book 3', 3, null), 
('Book 4', 1, null), 
('Book 5', 2, null);

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
