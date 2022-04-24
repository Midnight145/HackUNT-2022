import sqlite3

import threading

mutex = threading.Lock()

DATABASE_FILE = r"C:\Users\Midnight\Documents\Development\HackUNT-2022\server\server.db"

connection = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
connection.row_factory = sqlite3.Row
db = connection.cursor()


def init():
    db.execute("CREATE TABLE IF NOT EXISTS logins (uuid TEXT PRIMARY KEY, username TEXT, password TEXT, salt TEXT)")
    # todo: populate this table
    db.execute("CREATE TABLE IF NOT EXISTS users (uuid TEXT PRIMARY KEY, name TEXT, age INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS movie_reservations (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT, "
               "movie_id TEXT, date TEXT, time TEXT, theater INTEGER, seats INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, rating TEXT, "
               "showtime TEXT, showdate TEXT, theater INTEGER, seats BLOB, availabie INTEGER, capacity INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS theaters (id INTEGER PRIMARY KEY AUTOINCREMENT, capacity INTEGER, "
               "available INTEGER, theater_name TEXT, seats BLOB)")
    db.execute("CREATE TABLE IF NOT EXISTS admins (uuid TEXT PRIMARY KEY)")

    connection.commit()


def add_user(uuid, name, age):
    with mutex:
        db.execute("INSERT INTO users VALUES (?, ?, ?)", (uuid, name, age))
        connection.commit()


def add_theater(capacity, available, theater_name, seats):
    with mutex:
        db.execute("INSERT INTO theaters VALUES (?, ?, ?, ?)", (capacity, available, theater_name, seats))
        connection.commit()


def add_movie(title, rating, showtime, showdate, theater, seats):
    with mutex:
        # ugly constant is empty seats

        db.execute("INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?)", (title, rating, showtime, showdate, theater, str(chr(0)) * 100))
        connection.commit()


def add_admin(uuid):
    with mutex:
        db.execute("INSERT INTO admins VALUES (?)", (uuid,))
        connection.commit()


def get_user_by_uuid(uuid):
    resp = db.execute("SELECT * FROM users WHERE uuid = ?", (uuid,))
    return resp.fetchone()


def get_user_by_name(username):
    with mutex:
        print(username)
        resp = db.execute("SELECT * FROM users").fetchall()
        print("len:",len(resp))
        resp = db.execute("SELECT * FROM users WHERE name like ?", (username,))
    return resp.fetchone()


def add_reservation(uuid_, movie_id, date, time, theater, seats):
    with mutex:
        db.execute("INSERT INTO movie_reservations VALUES (?, ?, ?, ?, ?, ?, ?)", (uuid_, movie_id, date, time, theater, seats))
        connection.commit()


def get_movie_by_id(movie_id):
    with mutex:
        resp = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    return resp.fetchone()


def get_theater_by_name(theater_name):
    with mutex:
        resp = db.execute("SELECT * FROM theaters WHERE theater_name = ?", (theater_name,))
    return resp.fetchone()


def update_movie_seats(movie_id, seats):
    with mutex:
        db.execute("UPDATE movies SET seats = ? WHERE id = ?", (seats, movie_id))
        connection.commit()


def is_admin(uuid):
    with mutex:
        resp = db.execute("SELECT * FROM admins WHERE uuid = ?", (uuid,))
    return resp.fetchone() is not None


def execute(query):
    with mutex:
        db.execute(query)
        connection.commit()


def update_movie_availability(movie_id, available):
    with mutex:
        db.execute("UPDATE movies SET available = ? WHERE id = ?", (available, movie_id))
        connection.commit()


def get_movies():
    with mutex:
        resp = db.execute("SELECT * FROM movies")
    return resp.fetchall()


def get_reservations(uuid):
    with mutex:
        resp = db.execute("SELECT * FROM movie_reservations WHERE uuid = ?", (uuid,))
    return resp.fetchall()
