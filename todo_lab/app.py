import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Нужен для сообщений flash
DB_NAME = "todo.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

# Инициализация БД (если вдруг таблицы нет)
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Добавляем поле is_done, если его нет (безопасная операция)
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT, is_done INTEGER DEFAULT 0)")
    # Проверка на наличие колонки is_done для старых баз
    try:
        cursor.execute("ALTER TABLE tasks ADD COLUMN is_done INTEGER DEFAULT 0")
    except:
        pass
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, is_done FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Введите название задачи!", "danger") # Сообщение об ошибке
        return redirect(url_for("index"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, is_done) VALUES (?, 0)", (title,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET is_done = NOT is_done WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
