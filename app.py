import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, get_access_token, search_flight_offers
from datetime import datetime

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///travel_planner.db")

# Only run this part once to avoid recreating the table every time the app runs
if not os.path.exists('travel_planner.db'):
    db.execute("DROP TABLE IF EXISTS users")
    # Create the users table with a unique constraint on the email column
    db.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        hash TEXT NOT NULL
    )
    """)
    print("Database table 'users' created successfully.")

# API credentials
api_key = 'OH2gNvhJ6PndNemCKaRRy1e8rbWrEMGr'
api_secret = 'ErOvrIQByOXl1ktX'

# Get access token
access_token = get_access_token(api_key, api_secret)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure email was submitted
        if not email:
            return apology("must provide email", 403)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 403)

        # Ensure password confirmation matches
        if password != confirmation:
            return apology("passwords do not match", 403)

        # Hash password
        hash = generate_password_hash(password)

        # Insert user into database
        try:
            result = db.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", username, email, hash)
        except ValueError as e:
            print(f"Error: {e}")
            return apology("username or email already exists", 403)

        # Redirect user to login page
        flash('Account created successfully!')
        return redirect('/login')
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Forget any user_id
    session.clear()

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Ensure email was submitted
        if not email:
            return apology("must provide email", 403)

        # Ensure password was submitted
        if not password:
            return apology("must provide password", 403)

        # Query database for user
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)

        # Debug print statements
        print(f"Query result: {rows}")

        if len(rows) == 1:
            stored_hash = rows[0]['hash']
            print(f"Stored hash: {stored_hash}")
            password_match = check_password_hash(stored_hash, password)
            print(f"Password match: {password_match}")

        # Ensure user exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid email and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect('/')

    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    # Forget any user_id
    session.clear()
    return redirect('/')

@app.route('/search_flights', methods=['GET', 'POST'])
@login_required
def search_flights():
    if request.method == 'POST':
        origin = request.form.get('origin')
        destination = request.form.get('destination')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')

        flights = search_flight_offers(access_token, origin, destination, departure_date, return_date)

        # Format times
        for flight in flights['data']:
            for itinerary in flight['itineraries']:
                for segment in itinerary['segments']:
                    segment['departure']['time'] = datetime.fromisoformat(segment['departure']['at']).strftime('%H:%M')
                    segment['arrival']['time'] = datetime.fromisoformat(segment['arrival']['at']).strftime('%H:%M')

        # Save flights in session for pagination
        session['flights'] = flights['data']
        return redirect(url_for('search_flights', page=1))

    page = request.args.get('page', 1, type=int)
    per_page = 5  # Number of flights per page
    flights = session.get('flights', [])

    total_flights = len(flights)
    flights_paginated = flights[(page-1)*per_page:page*per_page]

    return render_template('search_flights.html', flights=flights_paginated, page=page, total_flights=total_flights, per_page=per_page)

if __name__ == '__main__':
    app.run(debug=True)
