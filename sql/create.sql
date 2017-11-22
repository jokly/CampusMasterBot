DROP TABLE Complaints;
DROP TABLE Users;

CREATE TABLE Users (
    chat_id          INT      NOT NULL PRIMARY KEY,
    telephone_number CHAR(12) NOT NULL,
    room             CHAR(5)
);

CREATE TABLE Complaints (
    chat_id INT       NOT NULL REFERENCES Users(chat_id),
    text    CHAR(200) NOT NULL
);