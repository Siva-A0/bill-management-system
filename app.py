from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

def init_db():
    conn = sqlite3.connect("bills.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            paid_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
    
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("bills.db")
        cursor = conn.cursor()

        try:

            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
            
        except:
            return "Username already exists."

        conn.close()
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("bills.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bills WHERE user_id = ?", (session["user_id"],))
    bills = cursor.fetchall()

    conn.close()

    return render_template("index.html", bills=bills)

@app.route("/add", methods=["GET", "POST"])
def add_bill():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        amount = request.form["amount"]
        due_date = request.form["due_date"]

        conn = sqlite3.connect("bills.db")
        cursor = conn.cursor()

        cursor.execute(
        "INSERT INTO bills (user_id, title, amount, due_date) VALUES (?, ?, ?, ?)",
        (session["user_id"], title, amount, due_date)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("add_bill"))

    return render_template("add_bill.html")

from datetime import datetime

@app.route("/pay/<int:bill_id>", methods=["POST"])
def pay_bill(bill_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    conn = sqlite3.connect("bills.db")
    cursor = conn.cursor()

    # Check current status
    cursor.execute(
        "SELECT status FROM bills WHERE id = ? AND user_id = ?",
        (bill_id, session["user_id"])
    )    
    result = cursor.fetchone()

    if result:
        if result[0] == "Pending":
            paid_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute(
                "UPDATE bills SET status = 'Paid', paid_at = ? WHERE id = ?",
                (paid_time, bill_id)
            )
            conn.commit()
    else:
        print("Bill already paid.")

    conn.close()

    return redirect(url_for("home"))

@app.route("/delete/<int:bill_id>", methods=["POST"])
def delete_bill(bill_id):
    conn = sqlite3.connect("bills.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM bills WHERE id = ? AND user_id = ?",
        (bill_id, session["user_id"])
    )
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("bills.db")
        cursor = conn.cursor()

        # Fetch user by username only
        cursor.execute(
            "SELECT id, password FROM users WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()
        conn.close()

        # Check if user exists AND password matches hash
        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect(url_for("home"))
        else:
            return "Invalid credentials."

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)