"""
Practice Script 2: Advanced SQLite
JOIN queries, aggregation, and more
"""
import sqlite3
import os

os.makedirs("data", exist_ok=True)
db = sqlite3.connect("data/practice2.db")
db.row_factory = sqlite3.Row
cursor = db.cursor()

# Create tables with relationships
print("=== Creating Related Tables ===")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author_id INTEGER,
        pages INTEGER,
        FOREIGN KEY (author_id) REFERENCES authors(id)
    )
""")
print("✅ Tables created!\n")

# Insert data
print("=== Inserting Data ===")
cursor.execute("INSERT INTO authors (name) VALUES (?)", ("J.K. Rowling",))
cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Tolkien",))

cursor.execute("INSERT INTO books (title, author_id, pages) VALUES (?, ?, ?)", ("Harry Potter", 1, 300))
cursor.execute("INSERT INTO books (title, author_id, pages) VALUES (?, ?, ?)", ("Chamber of Secrets", 1, 350))
cursor.execute("INSERT INTO books (title, author_id, pages) VALUES (?, ?, ?)", ("Lord of the Rings", 2, 500))
db.commit()
print("✅ Data inserted!\n")

# JOIN query
print("=== JOIN Query (Books with Authors) ===")
cursor.execute("""
    SELECT b.title, a.name as author, b.pages
    FROM books b
    JOIN authors a ON b.author_id = a.id
""")
for row in cursor.fetchall():
    print(f"  '{row['title']}' by {row['author']} ({row['pages']} pages)")
print()

# Aggregation
print("=== Aggregation Queries ===")
cursor.execute("SELECT COUNT(*) as total FROM books")
print(f"  Total books: {cursor.fetchone()['total']}")

cursor.execute("SELECT AVG(pages) as avg_pages FROM books")
print(f"  Average pages: {round(cursor.fetchone()['avg_pages'])}")

cursor.execute("""
    SELECT a.name, COUNT(b.id) as book_count
    FROM authors a
    LEFT JOIN books b ON a.id = b.author_id
    GROUP BY a.id
""")
print("\n  Books per author:")
for row in cursor.fetchall():
    print(f"    {row['name']}: {row['book_count']} books")
print()

# LIKE search
print("=== LIKE Search ===")
cursor.execute("SELECT title FROM books WHERE title LIKE ?", ("%Harry%",))
for row in cursor.fetchall():
    print(f"  Found: {row['title']}")
print()

db.close()
os.remove("data/practice2.db")
print("✅ Advanced SQLite learned!")
print("✅ Practice database cleaned up!")
