"""
Practice Script 1: SQLite Basics
Learn how SQLite works in Python
"""
import sqlite3
import os

# Create a practice database
os.makedirs("data", exist_ok=True)
db = sqlite3.connect("data/practice.db")
cursor = db.cursor()

# Create a simple table
print("=== Creating Table ===")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        grade TEXT
    )
""")
print("✅ Table created!\n")

# Insert data
print("=== Inserting Data ===")
cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ("Kashan", 20, "A"))
cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ("Ali", 22, "B"))
cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", ("Sara", 21, "A"))
db.commit()
print("✅ 3 students inserted!\n")

# Read data
print("=== Reading Data ===")
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
for row in rows:
    print(f"  ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Grade: {row[3]}")
print()

# Search data
print("=== Searching (Grade A) ===")
cursor.execute("SELECT * FROM students WHERE grade = ?", ("A",))
rows = cursor.fetchall()
for row in rows:
    print(f"  {row[1]} — Grade {row[3]}")
print()

# Update data
print("=== Updating Data ===")
cursor.execute("UPDATE students SET grade = ? WHERE name = ?", ("A+", "Kashan"))
db.commit()
cursor.execute("SELECT * FROM students WHERE name = ?", ("Kashan",))
row = cursor.fetchone()
print(f"  Kashan's new grade: {row[3]}\n")

# Delete data
print("=== Deleting Data ===")
cursor.execute("DELETE FROM students WHERE name = ?", ("Ali",))
db.commit()
cursor.execute("SELECT COUNT(*) FROM students")
count = cursor.fetchone()[0]
print(f"  Students remaining: {count}\n")

# Close
db.close()

# Cleanup
os.remove("data/practice.db")
print("✅ All SQLite basics learned!")
print("✅ Practice database cleaned up!")
