import os
from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv

from db import get_connection

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    return redirect(url_for("library"))


def render_library(author_form=None, author_errors=None, book_form=None, book_errors=None,
                   author_edit_error=None, book_edit_error=None):
    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT author_id, name, country FROM AUTHOR ORDER BY author_id")
        authors = cursor.fetchall()
        cursor.execute("SELECT book_id, title, price, author_id FROM BOOK ORDER BY book_id")
        books = cursor.fetchall()
    finally:
        conn.close()

    return render_template(
        "library.html",
        authors=authors,
        books=books,
        author_form=author_form or {},
        author_errors=author_errors or {},
        book_form=book_form or {},
        book_errors=book_errors or {},
        author_edit_error=author_edit_error,
        book_edit_error=book_edit_error,
    )


@app.route("/library")
def library():
    return render_library()


@app.route("/library/authors/add", methods=["POST"])
def add_author():
    name = request.form.get("name", "").strip()
    country = request.form.get("country", "").strip()

    if not name:
        return render_library(
            author_form={"name": name, "country": country},
            author_errors={"name": "Name is required"},
        )
    if len(name) > 100:
        return render_library(
            author_form={"name": name, "country": country},
            author_errors={"name": "Name is too long (100 characters at most)"},
        )

    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO AUTHOR (name, country) VALUES (?, ?)",
            (name, country or None),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))


@app.route("/library/books/add", methods=["POST"])
def add_book():
    title = request.form.get("title", "").strip()
    price = request.form.get("price", "").strip()
    author_id = request.form.get("author_id", "").strip()

    form = {"title": title, "price": price, "author_id": author_id}
    errors = {}

    if not title:
        errors["title"] = "Title is required"
    elif len(title) > 150:
        errors["title"] = "Title is too long (150 characters at most)"

    if not price:
        errors["price"] = "Price is required"
    else:
        try:
            if float(price) < 0:
                errors["price"] = "Price cannot be negative"
        except ValueError:
            errors["price"] = "Price must be a number"

    if not author_id:
        errors["author_id"] = "Author is required"

    if errors:
        return render_library(book_form=form, book_errors=errors)

    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO BOOK (title, price, author_id) VALUES (?, ?, ?)",
            (title, price, int(author_id)),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))


@app.route("/library/authors/<int:author_id>/edit", methods=["POST"])
def edit_author(author_id):
    name = request.form.get("name", "").strip()
    country = request.form.get("country", "").strip()

    if not name:
        return render_library(author_edit_error="Author name is required")
    if len(name) > 100:
        return render_library(author_edit_error="Author name is too long (100 characters at most)")

    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE AUTHOR SET name = ?, country = ? WHERE author_id = ?",
            (name, country or None, author_id),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))


@app.route("/library/books/<int:book_id>/edit", methods=["POST"])
def edit_book(book_id):
    title = request.form.get("title", "").strip()
    price = request.form.get("price", "").strip()
    author_id = request.form.get("author_id", "").strip()

    if not title:
        return render_library(book_edit_error="Book title is required")
    if len(title) > 150:
        return render_library(book_edit_error="Book title is too long (150 characters at most)")
    try:
        if float(price) < 0:
            return render_library(book_edit_error="Price cannot be negative")
    except ValueError:
        return render_library(book_edit_error="Price must be a number")
    if not author_id:
        return render_library(book_edit_error="Author is required")

    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE BOOK SET title = ?, price = ?, author_id = ? WHERE book_id = ?",
            (title, price, int(author_id), book_id),
        )
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))


@app.route("/library/books/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM BOOK WHERE book_id = ?", (book_id,))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))


@app.route("/library/authors/<int:author_id>/delete", methods=["POST"])
def delete_author(author_id):
    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM AUTHOR WHERE author_id = ?", (author_id,))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("library"))


# F2.1  Search books
@app.route("/library/search")
def search_books():
    title = request.args.get("title", "").strip()
    min_price = request.args.get("min_price", "").strip()
    max_price = request.args.get("max_price", "").strip()
    category_id = request.args.get("category_id", "").strip()
    searched = request.args.get("searched") == "1"

    form = {"title": title, "min_price": min_price,
            "max_price": max_price, "category_id": category_id}
    errors = {}

    try:
        min_val = float(min_price) if min_price else 0
    except ValueError:
        errors["min_price"] = "Minimum price must be a number"
        min_val = 0
    try:
        max_val = float(max_price) if max_price else 999999
    except ValueError:
        errors["max_price"] = "Maximum price must be a number"
        max_val = 999999
    if not errors and min_val > max_val:
        errors["max_price"] = "Maximum price must be at least the minimum"

    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT category_id, name FROM CATEGORY ORDER BY name")
        categories = cursor.fetchall()

        books = []
        if searched and not errors:
            cursor.execute(
                "SELECT b.book_id, b.title, b.price, c.name AS category "
                "FROM BOOK b "
                "JOIN CATEGORY c ON b.category_id = c.category_id "
                "WHERE b.title LIKE ? "
                "AND b.price BETWEEN ? AND ? "
                "AND (? = '' OR b.category_id = TRY_CAST(? AS INT)) "
                "ORDER BY b.price ASC",
                ("%" + title + "%", min_val, max_val, category_id, category_id),
            )
            books = cursor.fetchall()
    finally:
        conn.close()

    return render_template("search.html", form=form, errors=errors,
                           categories=categories, books=books, searched=searched)


# F2.2  Catalogue
@app.route("/library/catalogue")
def catalogue():
    conn = get_connection("library")
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT b.book_id, b.title, b.price, b.publish_year, "
            "a.name AS author, p.name AS publisher, c.name AS category "
            "FROM BOOK b "
            "JOIN AUTHOR a ON b.author_id = a.author_id "
            "JOIN PUBLISHER p ON b.publisher_id = p.publisher_id "
            "JOIN CATEGORY c ON b.category_id = c.category_id "
            "ORDER BY b.book_id"
        )
        books = cursor.fetchall()
    finally:
        conn.close()

    return render_template("catalogue.html", books=books)


# F2.3  Reports
@app.route("/library/reports")
def reports():
    conn = get_connection("library")
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT c.name AS category, COUNT(*) AS books, AVG(b.price) AS avg_price "
            "FROM BOOK b "
            "JOIN CATEGORY c ON b.category_id = c.category_id "
            "GROUP BY c.name "
            "ORDER BY c.name"
        )
        by_category = cursor.fetchall()

        cursor.execute(
            "SELECT a.name AS author, COUNT(*) AS books "
            "FROM AUTHOR a "
            "JOIN BOOK b ON b.author_id = a.author_id "
            "GROUP BY a.author_id, a.name "
            "HAVING COUNT(*) >= 2 "
            "ORDER BY a.name"
        )
        prolific = cursor.fetchall()

        cursor.execute(
            "SELECT SUM(price) AS total_price, MIN(price) AS min_price, "
            "MAX(price) AS max_price FROM BOOK"
        )
        totals = cursor.fetchone()
    finally:
        conn.close()

    return render_template("reports.html", by_category=by_category,
                           prolific=prolific, totals=totals)


# F2.4  Loans
@app.route("/library/loans")
def loans():
    conn = get_connection("library")
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT l.loan_id, b.title, m.name AS member, l.loan_date "
            "FROM LOAN l "
            "JOIN BOOK b ON l.book_id = b.book_id "
            "JOIN MEMBER m ON l.member_id = m.member_id "
            "WHERE l.return_date IS NULL "
            "ORDER BY l.loan_date"
        )
        not_returned = cursor.fetchall()

        cursor.execute(
            "SELECT m.member_id, m.name "
            "FROM MEMBER m "
            "LEFT JOIN LOAN l ON l.member_id = m.member_id "
            "WHERE l.loan_id IS NULL "
            "ORDER BY m.member_id"
        )
        no_loan_members = cursor.fetchall()

        cursor.execute(
            "SELECT b.book_id, b.title "
            "FROM BOOK b "
            "LEFT JOIN LOAN l ON l.book_id = b.book_id "
            "WHERE l.loan_id IS NULL "
            "ORDER BY b.book_id"
        )
        never_borrowed = cursor.fetchall()
    finally:
        conn.close()

    return render_template("loans.html", not_returned=not_returned,
                           no_loan_members=no_loan_members,
                           never_borrowed=never_borrowed)


# F2.5  Most borrowed
@app.route("/library/most-borrowed")
def most_borrowed():
    conn = get_connection("library")
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT TOP 3 b.title, COUNT(*) AS loans "
            "FROM BOOK b "
            "JOIN LOAN l ON l.book_id = b.book_id "
            "GROUP BY b.book_id, b.title "
            "ORDER BY COUNT(*) DESC"
        )
        top_books = cursor.fetchall()

        cursor.execute(
            "SELECT TOP 1 m.name AS member, COUNT(*) AS loans "
            "FROM MEMBER m "
            "JOIN LOAN l ON l.member_id = m.member_id "
            "GROUP BY m.member_id, m.name "
            "ORDER BY COUNT(*) DESC"
        )
        top_member = cursor.fetchone()
    finally:
        conn.close()

    return render_template("most_borrowed.html", top_books=top_books,
                           top_member=top_member)


# F2.6  Authors and books
@app.route("/library/authors-books")
def authors_books():
    conn = get_connection("library")
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT a.name AS author, COUNT(b.book_id) AS books "
            "FROM AUTHOR a "
            "LEFT JOIN BOOK b ON b.author_id = a.author_id "
            "GROUP BY a.author_id, a.name "
            "ORDER BY a.author_id"
        )
        author_counts = cursor.fetchall()

        cursor.execute(
            "SELECT b.title, a.name AS author, p.name AS publisher, a.country "
            "FROM BOOK b "
            "JOIN AUTHOR a ON b.author_id = a.author_id "
            "JOIN PUBLISHER p ON b.publisher_id = p.publisher_id "
            "WHERE a.country = p.country "
            "ORDER BY b.title"
        )
        same_country = cursor.fetchall()
    finally:
        conn.close()

    return render_template("authors_books.html", author_counts=author_counts,
                           same_country=same_country)


if __name__ == "__main__":
    app.run(debug=True)