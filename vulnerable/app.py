import sqlite3
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "MySecretKeyIsSOPrettyButSecret"

def get_db(): 
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():   
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            note_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["username"]
        pw = request.form["password"]
        hashed = generate_password_hash(pw)

        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (name, hashed),
            )
            db.commit()
        except sqlite3.IntegrityError:
            db.close()
            flash("That username is already taken")
            return redirect("/register")

        db.close()
        flash("Account created, please log in")
        return redirect("/login")

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["username"]
        pw = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (name,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user["password_hash"], pw):
            session["user_id"] = user["user_id"]
            return redirect("/notes")

        flash("Wrong username or password")
        return redirect("/login")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/notes")
def notes():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    rows = db.execute(
        "SELECT * FROM notes WHERE user_id = ?", (session["user_id"],)
    ).fetchall()
    db.close()

    return render_template("notes.html", notes=rows)


@app.route("/add", methods=["GET", "POST"])
def add_note():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        db = get_db()
        db.execute(
            "INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)",
            (session["user_id"], title, content),
        )
        db.commit()
        db.close()

        flash("Note saved")
        return redirect("/notes")

    return render_template("add_note.html")


@app.route("/note/<int:note_id>")
def view_note(note_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    note = db.execute(
        "SELECT * FROM notes WHERE note_id = ? AND user_id = ?",
        (note_id, session["user_id"]),
    ).fetchone()
    db.close()

    if note is None:
        flash("Note not found")
        return redirect("/notes")

    return render_template("view_note.html", note=note)


@app.route("/delete/<int:note_id>", methods=["POST"])
def delete_note(note_id):
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    db.execute(
        "DELETE FROM notes WHERE note_id = ? AND user_id = ?",
        (note_id, session["user_id"]),
    )
    db.commit()
    db.close()

    flash("Note deleted")
    return redirect("/notes")

if __name__ == "__main__":
    init_db()
    app.run(port=5001, debug=True)