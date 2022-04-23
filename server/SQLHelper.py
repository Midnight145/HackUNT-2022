import sqlite3

import threading

mutex = threading.Lock()

DATABASE_FILE = r"C:\Users\Midnight\Documents\Development\HackUNT-2022\server\server.db"

connection = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
db = connection.cursor()


def init():
    db.execute("CREATE TABLE IF NOT EXISTS users (uuid TEXT PRIMARY KEY, username TEXT, email TEXT, password TEXT, salt TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS movie_reservations (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT, movie_id TEXT, date TEXT, time TEXT, seats INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, rating TEXT, seats INTEGER)")
    # db.execute("CREATE TABLE IF NOT EXISTS reservations")
    connection.commit()


def add_user(uuid, username, email, password, salt):
    with mutex:
        db.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (uuid, username, email, password, salt))
        connection.commit()


def get_user_by_uuid(uuid):
    resp = db.execute("SELECT * FROM users WHERE uuid = ?", (uuid,))
    print(resp)
    print(resp.fetchone())
    return resp.fetchone()


def get_user_by_name(username):
    with mutex:
        print(username)
        resp = db.execute("SELECT * FROM users").fetchall()
        print("len:",len(resp))
        resp = db.execute("SELECT * FROM users WHERE username like ?", (username,))
    return resp.fetchone()


def add_reservation():
    pass