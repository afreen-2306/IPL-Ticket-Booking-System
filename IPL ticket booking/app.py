from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "Iplsecretkey"

# Database Connection
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        conn = get_db_connection()
        conn.execute("""
        INSERT INTO users(username,email,phone,password)
        VALUES(?,?,?,?)
        """,(username,email,phone,password))
        conn.commit()
        conn.close()
        flash("Registration Successful!")
        return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        conn=get_db_connection()
        user=conn.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email,password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"]=user["id"]
            session["username"]=user["username"]
            return redirect(url_for("home"))
        else:
            flash("Invalid Email or Password")

    return render_template("login.html")

@app.route("/matches")
def matches():
        conn = get_db_connection()
        matches = conn.execute("SELECT * FROM matches").fetchall()
        conn.close()
        return render_template("matches.html", matches=matches)

@app.route("/book/<int:match_id>", methods=["GET", "POST"])
def book_ticket(match_id):

    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    conn = get_db_connection()

    match = conn.execute(
        "SELECT * FROM matches WHERE id=?",
        (match_id,)
    ).fetchone()

    if request.method == "POST":

        quantity = int(request.form["quantity"])

        if quantity > match["available_seats"]:
            flash("Not enough seats available.")
            return redirect(url_for("book_ticket", match_id=match_id))

        seat_category = request.form["seat_category"]
        seat_numbers = request.form["seat_number"]

        if seat_category == "Business":
            price = 3000
        elif seat_category == "Premium":
            price = 2000
        else:
            price = 1000
        total_price = quantity * price

        conn.execute("""
        INSERT INTO bookings
        (user_id, match_id, seat_category, seat_number, quantity, total_price, booking_date)
        VALUES (?, ?, ?, ?, ?, ?, DATE('now'))
        """, (
            session["user_id"],
            match_id,
            seat_category,
            seat_numbers,
            quantity,
            total_price
        ))
        conn.execute("""
            UPDATE matches
            SET available_seats = available_seats - ?
            WHERE id = ?
        """, (
            quantity,
            match_id
        ))

        conn.commit()
        conn.close()

        flash("Ticket booked successfully!")

        return redirect(url_for("matches"))

    conn.close()

    return render_template("booking.html", match=match)

@app.route("/my_bookings")
def my_bookings():

    if "user_id" not in session:
        flash("Please login first.")
        return redirect(url_for("login"))

    conn = get_db_connection()

    bookings = conn.execute("""
        SELECT
            bookings.id,
            matches.team1,
            matches.team2,
            matches.stadium,
            matches.match_date,
            matches.match_time,
            bookings.quantity,
            bookings.total_price,
            bookings.booking_date
        FROM bookings
        JOIN matches
            ON bookings.match_id = matches.id
        WHERE bookings.user_id = ?
        ORDER BY bookings.booking_date DESC
    """, (session["user_id"],)).fetchall()

    conn.close()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )

@app.route("/all_bookings")
def all_bookings():

    conn = get_db_connection()

    bookings = conn.execute("""
        SELECT
            users.username,
            users.email,
            matches.team1,
            matches.team2,
            matches.stadium,
            matches.match_date,
            bookings.quantity,
            bookings.total_price,
            bookings.booking_date
        FROM bookings
        JOIN users
            ON bookings.user_id = users.id
        JOIN matches
            ON bookings.match_id = matches.id
        ORDER BY bookings.booking_date DESC
    """).fetchall()

    conn.close()

    return render_template(
        "all_bookings.html",
        bookings=bookings
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)