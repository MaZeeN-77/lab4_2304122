# Lab 4: Library Database and Website

Introduction to Database Systems, Alexandria National University, Fall 2026
Student ID: 2304122

Problem 2 only (Library). Database: Microsoft SQL Server. Website: Python Flask with pyodbc.

## Files

- `problem2_DDL.sql`: drops and creates the `library` database with 6 tables: AUTHOR, PUBLISHER, CATEGORY, BOOK, MEMBER, LOAN. Primary keys, foreign keys, and `ON DELETE CASCADE` on BOOK.author_id and LOAN.book_id.
- `problem2_DML.sql`: seed data: 5 authors, 3 publishers, 3 categories, 10 books, 5 members, 12 loans.
- `problem2_Queries.sql`: the SQL of pages F2.1 to F2.6, each marked with a `-- F2.x` comment.
- `website/`: the Flask website.

## Seed data coverage

- Two authors from the same country (George Orwell and Jane Austen, UK).
- An author with no books (Haruki Murakami).
- Authors with at least 2 books (Orwell, Austen, Mahfouz, Marquez).
- Authors and publishers from the same country (UK with Penguin Books, Egypt with Dar El Shorouk).
- A book priced between 15 and 20 (Pride and Prejudice, 17.50).
- Books never borrowed (Emma, Children of the Alley, One Hundred Years of Solitude, Love in the Time of Cholera).
- A member with no loans (Youssef Adel).
- Two loans not returned yet.

## Website pages

A navigation bar at the top of every page links to all of them.

| Page | URL | SQL features |
|---|---|---|
| Library (Lab 3: add, edit, delete books and authors) | `/library` | INSERT, UPDATE, DELETE |
| F2.1 Search books | `/library/search` | LIKE, BETWEEN, ORDER BY |
| F2.2 Catalogue | `/library/catalogue` | JOIN of 4 tables |
| F2.3 Reports | `/library/reports` | GROUP BY, HAVING, aggregates |
| F2.4 Loans | `/library/loans` | JOIN, LEFT JOIN |
| F2.5 Most borrowed | `/library/most-borrowed` | GROUP BY, ORDER BY, TOP |
| F2.6 Authors and books | `/library/authors-books` | LEFT JOIN, JOIN |

## Notes

- SQL Server has no `LIMIT`, so `TOP` is used in F2.5.
- Bonus: the search form in F2.1 uses prepared statements (`?` placeholders). The `LIKE` pattern is built in Python and passed as a parameter, never concatenated into the SQL text.
- Books added from the Lab 3 `/library` page have no publisher or category, so they do not appear in the catalogue or in the search results. `publisher_id` and `category_id` are nullable for this reason.
- The `.env` file is not included in the repository.
