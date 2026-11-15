USE library;
GO

DECLARE @title       VARCHAR(150)  = 'a';
DECLARE @min_price   DECIMAL(8,2)  = 10;
DECLARE @max_price   DECIMAL(8,2)  = 25;
DECLARE @category_id INT           = NULL;

SELECT b.book_id, b.title, b.price, c.name AS category
FROM BOOK b
JOIN CATEGORY c ON b.category_id = c.category_id
WHERE b.title LIKE '%' + @title + '%'
  AND b.price BETWEEN @min_price AND @max_price
  AND (@category_id IS NULL OR b.category_id = @category_id)
ORDER BY b.price ASC;
GO

SELECT b.book_id, b.title, b.price, b.publish_year,
       a.name AS author, p.name AS publisher, c.name AS category
FROM BOOK b
JOIN AUTHOR a    ON b.author_id    = a.author_id
JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
JOIN CATEGORY c  ON b.category_id  = c.category_id
ORDER BY b.book_id;
GO

SELECT c.name AS category, COUNT(*) AS books, AVG(b.price) AS avg_price
FROM BOOK b
JOIN CATEGORY c ON b.category_id = c.category_id
GROUP BY c.name;
GO

SELECT a.name AS author, COUNT(*) AS books
FROM AUTHOR a
JOIN BOOK b ON b.author_id = a.author_id
GROUP BY a.name
HAVING COUNT(*) >= 2;
GO

SELECT SUM(price) AS total_price, MIN(price) AS min_price, MAX(price) AS max_price
FROM BOOK;
GO

SELECT l.loan_id, b.title, m.name AS member, l.loan_date
FROM LOAN l
JOIN BOOK b   ON l.book_id   = b.book_id
JOIN MEMBER m ON l.member_id = m.member_id
WHERE l.return_date IS NULL;
GO

SELECT m.member_id, m.name
FROM MEMBER m
LEFT JOIN LOAN l ON l.member_id = m.member_id
WHERE l.loan_id IS NULL;
GO

SELECT b.book_id, b.title
FROM BOOK b
LEFT JOIN LOAN l ON l.book_id = b.book_id
WHERE l.loan_id IS NULL;
GO

SELECT TOP 3 b.title, COUNT(*) AS loans
FROM BOOK b
JOIN LOAN l ON l.book_id = b.book_id
GROUP BY b.book_id, b.title
ORDER BY COUNT(*) DESC;
GO

SELECT TOP 1 m.name AS member, COUNT(*) AS loans
FROM MEMBER m
JOIN LOAN l ON l.member_id = m.member_id
GROUP BY m.member_id, m.name
ORDER BY COUNT(*) DESC;
GO

SELECT a.name AS author, COUNT(b.book_id) AS books
FROM AUTHOR a
LEFT JOIN BOOK b ON b.author_id = a.author_id
GROUP BY a.author_id, a.name
ORDER BY a.author_id;
GO

SELECT b.title, a.name AS author, p.name AS publisher, a.country
FROM BOOK b
JOIN AUTHOR a    ON b.author_id    = a.author_id
JOIN PUBLISHER p ON b.publisher_id = p.publisher_id
WHERE a.country = p.country;
GO