import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DB_NAME = "todo.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

@app.route("/")
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    conn.close()

    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    if title == "":
        return redirect(url_for("index"))

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (title,))  #
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
