USE master;
GO

CREATE DATABASE library;
GO

USE library;
GO

CREATE TABLE AUTHOR (
    author_id INT          NOT NULL IDENTITY(1,1),
    name      VARCHAR(100) NOT NULL,
    country   VARCHAR(100) NULL,
    CONSTRAINT PK_AUTHOR PRIMARY KEY (author_id)
);
GO

CREATE TABLE PUBLISHER (
    publisher_id INT          NOT NULL IDENTITY(1,1),
    name         VARCHAR(100) NOT NULL,
    country      VARCHAR(100) NULL,
    CONSTRAINT PK_PUBLISHER PRIMARY KEY (publisher_id)
);
GO

CREATE TABLE CATEGORY (
    category_id INT          NOT NULL IDENTITY(1,1),
    name        VARCHAR(100) NOT NULL,
    CONSTRAINT PK_CATEGORY PRIMARY KEY (category_id),
    CONSTRAINT UQ_CATEGORY_name UNIQUE (name)
);
GO

CREATE TABLE BOOK (
    book_id      INT           NOT NULL IDENTITY(1,1),
    title        VARCHAR(150)  NOT NULL,
    price        DECIMAL(8,2)  NOT NULL,
    publish_year INT           NULL,
    author_id    INT           NOT NULL,
    publisher_id INT           NULL,
    category_id  INT           NULL,
    CONSTRAINT PK_BOOK PRIMARY KEY (book_id),
    CONSTRAINT CK_BOOK_price CHECK (price >= 0),
    CONSTRAINT FK_BOOK_AUTHOR FOREIGN KEY (author_id) REFERENCES AUTHOR(author_id) ON DELETE CASCADE,
    CONSTRAINT FK_BOOK_PUBLISHER FOREIGN KEY (publisher_id) REFERENCES PUBLISHER(publisher_id),
    CONSTRAINT FK_BOOK_CATEGORY FOREIGN KEY (category_id) REFERENCES CATEGORY(category_id)
);
GO

CREATE TABLE MEMBER (
    member_id INT          NOT NULL IDENTITY(1,1),
    name      VARCHAR(100) NOT NULL,
    email     VARCHAR(255) NOT NULL,
    join_date DATE         NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    CONSTRAINT PK_MEMBER PRIMARY KEY (member_id),
    CONSTRAINT UQ_MEMBER_email UNIQUE (email)
);
GO

CREATE TABLE LOAN (
    loan_id     INT  NOT NULL IDENTITY(1,1),
    book_id     INT  NOT NULL,
    member_id   INT  NOT NULL,
    loan_date   DATE NOT NULL,
    return_date DATE NULL, 
    CONSTRAINT PK_LOAN PRIMARY KEY (loan_id),
    CONSTRAINT CK_LOAN_dates CHECK (return_date IS NULL OR return_date >= loan_date),
    CONSTRAINT FK_LOAN_BOOK FOREIGN KEY (book_id) REFERENCES BOOK(book_id) ON DELETE CASCADE,
    CONSTRAINT FK_LOAN_MEMBER FOREIGN KEY (member_id) REFERENCES MEMBER(member_id)
);
GO