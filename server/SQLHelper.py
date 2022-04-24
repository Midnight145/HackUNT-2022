import sqlite3

import threading

mutex = threading.Lock()

DATABASE_FILE = r"C:\Users\Midnight\Documents\Development\HackUNT-2022\server\server.db"

connection: sqlite3.Connection = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
connection.row_factory = sqlite3.Row
db: sqlite3.Cursor = connection.cursor()


def init() -> None:
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


def add_user(uuid: str, name: str, age: int) -> None:
    with mutex:
        db.execute("INSERT INTO users VALUES (?, ?, ?)", (uuid, name, age))
        connection.commit()


def add_theater(capacity: int, available: int, theater_name: str, seats: str) -> None:
    with mutex:
        db.execute("INSERT INTO theaters VALUES (?, ?, ?, ?)", (capacity, available, theater_name, seats))
        connection.commit()


# todo: update this to use updated table
def add_movie(title: str, rating: str, showtime: int, showdate: int, theater: str, available: int, capacity: int) -> None:
    with mutex:
        # ugly constant is empty seats

        db.execute("INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?)", (title, rating, showtime, showdate, theater, str(chr(0)) * 100))
        connection.commit()


def add_admin(uuid: str) -> None:
    with mutex:
        db.execute("INSERT INTO admins VALUES (?)", (uuid,))
        connection.commit()


def get_user_by_uuid(uuid: str) -> sqlite3.Row:
    resp = db.execute("SELECT * FROM users WHERE uuid = ?", (uuid,))
    return resp.fetchone()


def get_user_by_name(username: str) -> sqlite3.Row:
    with mutex:
        print(username)
        resp = db.execute("SELECT * FROM users").fetchall()
        print("len:",len(resp))
        resp = db.execute("SELECT * FROM users WHERE name like ?", (username,))
    return resp.fetchone()


def add_reservation(uuid_: str, movie_id: int, date: int, time: int, theater: str, seats: str) -> None:
    with mutex:
        db.execute("INSERT INTO movie_reservations VALUES (?, ?, ?, ?, ?, ?)", (uuid_, movie_id, date, time, theater, seats))
        connection.commit()


def get_movie_by_id(movie_id: str) -> sqlite3.Row:
    with mutex:
        resp = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    return resp.fetchone()


def get_theater_by_name(theater_name: str) -> sqlite3.Row:
    with mutex:
        resp = db.execute("SELECT * FROM theaters WHERE theater_name = ?", (theater_name,))
    return resp.fetchone()


def update_movie_seats(movie_id: int, seats: str) -> None:
    with mutex:
        db.execute("UPDATE movies SET seats = ? WHERE id = ?", (seats, movie_id))
        connection.commit()


def is_admin(uuid: str) -> bool:
    with mutex:
        resp = db.execute("SELECT * FROM admins WHERE uuid = ?", (uuid,))
    return resp.fetchone() is not None


def execute(query: str) -> None:
    with mutex:
        db.execute(query)
        connection.commit()


def update_movie_availability(movie_id: int, available: int) -> None:
    with mutex:
        db.execute("UPDATE movies SET available = ? WHERE id = ?", (available, movie_id))
        connection.commit()


def get_unique_movies() -> set[str]:
    with mutex:
        resp = db.execute("SELECT title FROM movies")
    titles = []
    for row in resp.fetchall():
        titles.append(row["title"])
    return set(titles)


def get_movies() -> list[sqlite3.Row]:
    with mutex:
        resp = db.execute("SELECT * FROM movies")
    return resp.fetchall()


def get_movies_by_title(title: str) -> list[sqlite3.Row]:
    with mutex:
        resp = db.execute("SELECT * FROM movies WHERE title like ?", (title,))
    return resp.fetchall()


def get_reservations(uuid: str) -> list[sqlite3.Row]:
    with mutex:
        resp = db.execute("SELECT * FROM movie_reservations WHERE uuid = ?", (uuid,))
    return resp.fetchall()
