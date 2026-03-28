import sqlite3

DB_NAME = "todo.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS tasks ("  
    "id INTEGER PRIMARY KEY, "  
    "title TEXT"  
    ")"
)

cursor.execute(
    "INSERT INTO tasks (title) VALUES (?)",
    ("Купить молоко",)
)

cursor.execute(
    "INSERT INTO tasks (title) VALUES (?)",
    ("Сделать домашку",)
)

conn.commit()

cursor.execute("SELECT id, title FROM tasks")
rows = cursor.fetchall()

print("Задачи в базе данных:")
for row in rows:
    task_id = row[0]
    title = row[1]
    print(task_id, "-", title)

conn.close()
