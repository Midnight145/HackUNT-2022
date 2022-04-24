import sqlite3

import threading
import uuid

mutex = threading.Lock()

DATABASE_FILE = r"C:\Users\Midnight\Documents\Development\HackUNT-2022\server\server.db"

connection: sqlite3.Connection = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
connection.row_factory = sqlite3.Row
db: sqlite3.Cursor = connection.cursor()


def init() -> None:
    db.execute("CREATE TABLE IF NOT EXISTS users (uuid TEXT PRIMARY KEY, name TEXT, age INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS movie_reservations (id INTEGER PRIMARY KEY AUTOINCREMENT, uuid TEXT, "
               "movie_id TEXT, date TEXT, time TEXT, theater INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS movies (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, rating TEXT, "
               "date TEXT, time TEXT, theater INTEGER, available INTEGER, capacity INTEGER)")
    db.execute("CREATE TABLE IF NOT EXISTS theaters (id INTEGER PRIMARY KEY AUTOINCREMENT, capacity INTEGER, "
               "available INTEGER, theater_name TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS admins (uuid TEXT PRIMARY KEY)")
    db.execute("CREATE TABLE IF NOT EXISTS seats (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, reserved INTEGER, "
               "movie_id INTEGER, seat_number INTEGER)")

    connection.commit()


def create_user(name: str, age: int) -> str:
    """
    Creates a user and stores it in the database
    :param name: user's name
    :param age: user age
    :return: None
    """
    uuid_ = str(uuid.uuid4())
    with mutex:
        db.execute("INSERT INTO users (uuid, name, age) VALUES (?, ?, ?)", (uuid_, name, age))
        connection.commit()
    return uuid_


def add_theater(capacity: int, available: int, theater_name: str, seats: str) -> None:
    """
    Adds a theater to the database
    :param capacity: total seats
    :param available: available seats
    :param theater_name: theater name
    :param seats: current seats
    :return: None
    """
    with mutex:
        db.execute("INSERT INTO theaters (capacity, available, theater_name, seats) VALUES (?, ?, ?, ?)", (capacity, available, theater_name, seats))
        connection.commit()


def add_movie(title: str, rating: str, date: int, time: int, theater: str, available: int,
              capacity: int) -> int:
    """
    Adds a movie to the database
    :param title: the movie title
    :param rating: the movie rating
    :param time: movie time
    :param date: movie date
    :param theater: theater id
    :param available: available seats
    :param capacity: total seats
    :return: Created movie id
    """
    with mutex:
        db.execute("INSERT INTO movies (title, rating, date, time theater, available, capacity) VALUES (?, ?, ?, ?, ?, ?)",
                   (title, rating, date, time, theater, available, capacity))
        connection.commit()
        # get new movie id
        db.execute("SELECT FROM movies WHERE title = ?, rating = ?, date = ?, time = ?, theater = ?, "
                   "available = ?, capacity = ?", (title, rating, date, time, theater, available, capacity))
        new_movie_id = db.fetchone()["id"]
    return new_movie_id


def add_reservation(uuid_: str, movie_id: int, date: int, time: int, theater: str) -> None:
    """
    Adds a reservation to the database
    :param uuid_: user uuid
    :param movie_id: movie id
    :param date: the reservation date
    :param time: the reservation time
    :param theater: the theater id
    :return: None
    """
    with mutex:
        db.execute("INSERT INTO movie_reservations (uuid, movie_id, date, time, theater) VALUES (?, ?, ?, ?, ?)",
                   (uuid_, movie_id, date, time, theater))
        connection.commit()


def get_user_by_uuid(uuid: str) -> sqlite3.Row:
    """
    Gets the user by uuid
    :param uuid: user uuid
    :return: the user
    """
    with mutex:
        resp = db.execute("SELECT * FROM users WHERE uuid = ?", (uuid,))
    return resp.fetchone()


def get_movie_by_id(movie_id: str) -> sqlite3.Row:
    """
    Gets the movie by id
    :param movie_id: movie id
    :return: the movie
    """
    with mutex:
        resp = db.execute("SELECT * FROM movies WHERE id = ?", (movie_id,))
    return resp.fetchone()


def get_movie_seats(movie_id: int) -> list[sqlite3.Row]:
    """
    Gets the seats for a movie
    :param movie_id: movie id
    :return: all seats for a movie
    """
    with mutex:
        resp = db.execute("SELECT * FROM seats WHERE movie_id = ?", (movie_id,))
    return resp.fetchall()


def get_reserved_seats(movie_id: int) -> list[sqlite3.Row]:
    """
    Returns a list of all seats that are reserved for a movie.
    :param movie_id: movie id
    :return: List of reserved seats
    """
    with mutex:
        resp = db.execute("SELECT * FROM seats WHERE movie_id = ? AND reserved = 1", (movie_id,))
    return resp.fetchall()


def update_movie_availability(movie_id: int, available: int) -> None:
    """
    Updates the available seats for a movie
    :param movie_id: movie id
    :param available: number of available seats
    :return:
    """
    with mutex:
        db.execute("UPDATE movies SET available = ? WHERE id = ?", (available, movie_id))
        connection.commit()


def reserve_seats(uuid_: str, movie_id: int, seats: list[int]) -> None:
    """
    Will reserve seats for a user into the seats table.
    :param uuid_: the user's uuid
    :param movie_id: the id of the movie to reserve for
    :param seats: the list of seat numbers being reserved
    :return: None
    """
    with mutex:
        for i in seats:
            if db.execute("SELECT * FROM seats WHERE movie_id = ? AND seat_number = ?",
                          (movie_id, i)).fetchone() is None:
                db.execute("INSERT INTO seats (user, reserved, movie_id, seat_number) VALUES (?, ?, ?, ?)",
                           (uuid_, 1, movie_id, i))
            else:
                db.execute("UPDATE seats SET reserved = 1, user = ? WHERE movie_id = ? AND seat_number = ?",
                           (uuid_, movie_id, i))


def is_admin(uuid: str) -> bool:
    """
    Checks if the user is an admin
    :param uuid:
    :return: if the user is an admin
    """
    with mutex:
        resp = db.execute("SELECT * FROM admins WHERE uuid = ?", (uuid,))
    return resp.fetchone() is not None


# ALL RETURN COMMANDS BELOW THIS LINE

def get_unique_movies() -> set[str]:
    """
    Returns a set of all unique movie titles, eventually gets sent to the client
    :return: set of all unique movie titles
    """
    with mutex:
        resp = db.execute("SELECT title FROM movies")
    titles = []
    for row in resp.fetchall():
        titles.append(row["title"])
    return set(titles)


def get_movies() -> list[sqlite3.Row]:
    """
    Returns a list of all movies, eventually gets sent to the client
    :return: a list of all movies
    """
    with mutex:
        resp = db.execute("SELECT * FROM movies")
    return resp.fetchall()


def get_movies_by_title(title: str) -> list[sqlite3.Row]:
    """
    Returns a list of all movies with the given title, eventually gets sent to the client
    :param title:
    :return: a list of all movies with the given title
    """
    with mutex:
        resp = db.execute("SELECT * FROM movies WHERE title like ?", (title,))
    return resp.fetchall()


def get_reservations(uuid: str) -> list[sqlite3.Row]:
    """
    Returns a list of all reservations for the given user, eventually gets sent to the client
    :param uuid:
    :return: a list of all reservations for the given user
    """
    with mutex:
        resp = db.execute("SELECT * FROM movie_reservations WHERE uuid = ?", (uuid,))
    return resp.fetchall()


def get_seats(movie_id: int) -> list[sqlite3.Row]:
    """
    Returns a list of all seats for the given movie, eventually gets sent to the client
    :param movie_id:
    :return: a list of all seats for the given movie
    """
    with mutex:
        resp = db.execute("SELECT * FROM seats WHERE movie_id = ?", (movie_id,))
    return resp.fetchall()


def get_reservation(uuid: str, movie_id: int) -> sqlite3.Row:
    """
    Returns the reservation for the given user and movie, eventually gets sent to the client
    :param uuid:
    :param movie_id:
    :return: the reservation for the given user and movie
    """
    with mutex:
        resp = db.execute("SELECT * FROM movie_reservations WHERE uuid = ? AND movie_id = ?", (uuid, movie_id))
    return resp.fetchone()


def get_dates(movie_title) -> list[str]:
    """
    Returns a list of all dates for the given movie, eventually gets sent to the client
    :param movie_title: the title of the movie
    :return: a list of all dates for the given movie
    """
    with mutex:
        resp = db.execute("SELECT date FROM movies WHERE title = ?", (movie_title,))
    return [i["date"] for i in resp.fetchall()]


def get_times(movie_title, date) -> list[str]:
    """
    Returns a list of all times for the given movie, eventually gets sent to the client
    :param movie_title: the title of the movie
    :return: a list of all times for the given movie
    """
    with mutex:
        resp = db.execute("SELECT time FROM movies WHERE title = ? AND date = ?", (movie_title, date))
    return [i["time"] for i in resp.fetchall()]


def get_theaters() -> list[sqlite3.Row]:
    """
    Returns a list of all theaters, eventually gets sent to the client
    :return: a list of all theaters
    """
    with mutex:
        resp = db.execute("SELECT * FROM theaters")
    return resp.fetchall()