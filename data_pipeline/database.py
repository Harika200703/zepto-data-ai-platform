import sqlite3
import csv

connection = sqlite3.connect("data_pipeline/books.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_name TEXT NOT NULL UNIQUE
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    price_gbp REAL NOT NULL,
    price_inr REAL NOT NULL,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
)
""")
categories = ["Travel", "Mystery", "Science"]

for category in categories:
    cursor.execute(
        "INSERT OR IGNORE INTO categories (category_name) VALUES (?)",
        (category,)
    )
with open("data_pipeline/books.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    cursor.execute("DELETE FROM books")
    for book in reader:
        category_id = ((reader.line_num - 2) % 3) + 1

        cursor.execute("""
        INSERT INTO books (title, price_gbp, price_inr, category_id)
        VALUES (?, ?, ?, ?)
        """, (
        book["title"],
        book["price_gbp"],
        book["price_inr"],
        category_id
        ))

connection.commit()
connection.close()

print("Books inserted successfully")