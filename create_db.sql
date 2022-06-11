CREATE TABLE user(
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    phone_number INTEGER NOT NULL,
    address TEXT NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE wanted_book_list(
    wanted_book_list_id INTEGER NOT NULL,
    wanted_book_list_name TEXT NOT NULL,
    wanted_book_list_description TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (wanted_book_list_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE follows(
    user_id INTEGER NOT NULL,
    wanted_book_list_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, wanted_book_list_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (wanted_book_list_id) REFERENCES wanted_book_list(wanted_book_list_id)
);

CREATE TABLE book_wanted(
    book_id INTEGER NOT NULL,
    wanted_book_list_id NOT NULL,
    PRIMARY KEY (book_id, wanted_book_list_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id),
    FOREIGN KEY (wanted_book_list_id) REFERENCES wanted_book_list(wanted_book_list_id)
);

CREATE TABLE book(
    book_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    price REAL NOT NULL,
    edition TEXT NOT NULL,
    author TEXT NOT NULL,
    condition TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE publisher(
    publisher_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    book_id INTEGER NOT NULL,
    FOREIGN KEY (book_id) REFERENCES book(book_id)
);

CREATE TABLE lends_history(
    lend_id INTEGER NOT NULL,
    book_location TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    review_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id),
    FOREIGN KEY (review_id) REFERENCES book_reviews(review_id)
);

CREATE TABLE book_reviews(
    review_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    review TEXT NOT NULL,
    lend_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (lend_id) REFERENCES lends_history(lend_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

CREATE TABLE alumni_donors (
    donor_id INTEGER NOT NULL,
    name TEXT NOT NULL
);

CREATE TABLE donated(
    donor_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    PRIMARY KEY (donor_id, book_id),
    FOREIGN KEY (donor_id) REFERENCES alumni_donors(donor_id),
    FOREIGN KEY (book_id) REFERENCES book(book_id)
);

CREATE TABLE user_logs(
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL
);