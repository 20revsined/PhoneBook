PRAGMA foreign_keys = ON;

CREATE TABLE users (
    username VARCHAR(255) NOT NULL,
    password varchar(255) NOT NULL,
    PRIMARY KEY(username)
);

CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_owner VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    profile_picture VARCHAR(255) NOT NULL,
    phone_number VARCHAR(255) NOT NULL,
    email_address VARCHAR(255) NOT NULL,
    home_address VARCHAR(255) NOT NULL,
    FOREIGN KEY(contact_owner) REFERENCES users(username) ON DELETE CASCADE
);