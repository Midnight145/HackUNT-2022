from socket import socket
from typing import Union
from connection import Client
import SQLHelper


def reserve(client: Client, data: list[Union[str, int]]) -> str:
    if len(data) < 7:
        return "Invalid Parameters"
    uuid_ = data[0]
    date = data[2]
    time = data[3]
    theater = data[4]
    movie_id = data[5]
    seats = data[6:]  # all seats are this param or later

    print("Reserving seats")

    user = SQLHelper.get_user_by_uuid(client.uuid)
    movie = SQLHelper.get_movie_by_id(movie_id)
    reserved_seats = SQLHelper.get_reserved_seats(movie_id)
    reserved_seat_numbers = [i["seat_number"] for i in reserved_seats]

    if movie is None:  # movie does not exist
        return f"Movie with id {movie_id} not found"

    if any(i in reserved_seat_numbers for i in seats):  # seat is reserved
        return "Seat already reserved"

    # check rating
    if movie["rating"] == "R" or movie["rating"] == "NC-17" and user["age"] < 18:
        return "You are too young to reserve this movie"

    if len(seats) != len(set(seats)):  # duplicate seats
        return "Duplicate seats"

    if any(int(i) > 99 or int(i) < 0 for i in seats):  # seat number is out of range
        return "Invalid seat number"

    SQLHelper.reserve_seats(uuid_, movie_id, data[6:])  # reserve seats

    reserved_seats = SQLHelper.get_reserved_seats(movie_id)  # get reserved seats to get updated seat numbers

    SQLHelper.update_movie_availability(movie_id, 100 - len(
        reserved_seats))  # update movie availability-- subtract reserved seats from total seats

    SQLHelper.add_reservation(uuid_, movie_id, date, time, theater)  # add reservation

    return "Reserved"


def create(client: socket, data: list[Union[str, int]]) -> str:
    uuid = data[0]
    if not SQLHelper.is_admin(uuid):
        return "Permission denied"

    tablename = data[2]
    columns = data[3:]

    if tablename == "users":
        SQLHelper.add_user(columns[0], columns[1], columns[2])

    if tablename == "movies":
        SQLHelper.add_movie(columns[0], columns[1], columns[2], columns[3], columns[4])

    if tablename == "theaters":
        SQLHelper.add_theater(columns[0], columns[1], columns[2], columns[3])

    return "Table created"


# RESPONSES SENT TO CLIENT

def get_movies_by_title(client: socket, data: list[Union[str, int]]) -> str:
    if len(data) != 3:  # data[0] is uuid, data[1] is command, data[2] is title
        return "Invalid Parameters"
    title = data[2]  # title of movie

    movies = SQLHelper.get_movies_by_title(title)
    # todo: change what this returns
    movies = [i["title"] for i in movies]  # get titles
    return '::'.join(movies)


def get_unique_movies(client: socket, data: list[Union[str, int]]) -> str:
    if len(data) != 2:  # data[0] is uuid, data[1] is command-- no params
        return "Invalid Parameters"

    movies = list(SQLHelper.get_unique_movies())  # get all movies
    return '::'.join(movies)  # format for sending to client-- title1::title2::title3


def get_movies(client: socket, data: list[Union[str, int]]) -> str:
    if len(data) > 2:  # data[0] is uuid, data[1] is command-- no params
        return "Invalid Parameters"

    def movie_to_str(__movie):  # helper function to convert movie to string
        return (
            f"{__movie['id']}::{__movie['title']}::{__movie['rating']}::{__movie['showtime']}::{__movie['showdate']}"
            f"::{__movie['theater']}::{__movie['seats']}::{__movie['available']}::{__movie['capacity']}")

    movies = SQLHelper.get_movies()  # get all movies
    retval = ""  # return value
    for movie in movies:
        retval += movie_to_str(movie) + "\n"  # add movie to return value
    return retval


def get_reservations(client: socket, data: list[Union[str, int]]) -> str:
    if len(data) > 2:  # data[0] is uuid, data[1] is command-- no params
        return "Invalid Parameters"

    def reservation_to_str(__reservation):  # helper function to convert reservation to string
        return (
            f"{__reservation['id']}::{__reservation['movie_id']}::{__reservation['date']}::{__reservation['time']}"
            f"::{__reservation['theater']}::{__reservation['seats']}")

    reservations = SQLHelper.get_reservations(data[0])  # get reservations for user
    retval = ""
    for reservation in reservations:
        retval += reservation_to_str(reservation) + "\n"  # add reservation to return value
    return retval
