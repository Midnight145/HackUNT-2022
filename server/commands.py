from socket import socket
from typing import Union, TYPE_CHECKING
import SQLHelper

if TYPE_CHECKING:  # avoid circular import, always false
    from connection import Client


# todo: update responses to match new spec

def reserve(client: 'Client', data: list[Union[str, int]]) -> str:
    if len(data) < 7:
        return "failiure::Invalid Parameters"
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

    reserved_seat_numbers = [str(i["seat_number"]) for i in reserved_seats]
    print("reserved", reserved_seat_numbers)
    print("seats", seats)

    if movie is None:  # movie does not exist
        return f"failure::Movie with id {movie_id} not found"

    if any(i in reserved_seat_numbers for i in seats):  # seat is reserved
        return "failure::Seat already reserved"

    # check rating
    rating = movie["rating"].lower()
    if movie["rating"] == "r" or movie["rating"] == "nc-17" and user["age"] < 18:
        return "failure::You are too young to reserve this movie"

    if len(seats) != len(set(seats)):  # duplicate seats
        return "failure::Duplicate seats"

    if any(int(i) > 99 or int(i) < 0 for i in seats):  # seat number is out of range
        return "failure::Invalid seat number"

    SQLHelper.reserve_seats(uuid_, movie_id, data[6:])  # reserve seats

    reserved_seats = SQLHelper.get_reserved_seats(movie_id)  # get reserved seats to get updated seat numbers

    SQLHelper.update_movie_availability(movie_id, 100 - len(
        reserved_seats))  # update movie availability-- subtract reserved seats from total seats

    SQLHelper.add_reservation(uuid_, movie_id, date, time, theater)  # add reservation
    reservation_id = SQLHelper.get_reservation(uuid_, movie_id)["id"]  # get reservation to get id

    return f"success::{reservation_id}"


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
            f"::{__movie['theater']}::{__movie['available']}::{__movie['capacity']}")

    movies = SQLHelper.get_movies()  # get all movies
    retval = ""  # return value
    for movie in movies:
        retval += movie_to_str(movie) + "\n"  # add movie to return value
    return retval


def get_reservations(client: socket, data: list[Union[str, int]]) -> str:
    if len(data) > 2:  # data[0] is uuid, data[1] is command-- no params
        return "Invalid Parameters"

    def reservation_to_str(__reservation, seats):  # helper function to convert reservation to string
        return (
            f"{__reservation['id']}::{__reservation['movie_id']}::{__reservation['date']}::{__reservation['time']}"
            f"::{__reservation['theater']}::{'::'.join(seats)}")

    reservations = SQLHelper.get_reservations(data[0])  # get reservations for user

    retval = "reservationid::movieid::date::time::theater::seats\n"  # return value
    for reservation in reservations:
        all_seats = SQLHelper.get_reserved_seats(reservation["movie_id"])  # get reserved seats for user
        print("Checking if seats are available")
        print("Reserved seats:", [i["seat_number"] for i in all_seats])
        seats = []
        for seat in all_seats:
            print("seat_id:", seat["movie_id"])
            print(reservation["movie_id"] == seat["movie_id"])
            if int(reservation["movie_id"]) == int(seat["movie_id"]):
                print("in if")
                seats.append(str(seat["seat_number"]))
        print("movie_id:", reservation["movie_id"])
        print("Seats:", seats)
        retval += reservation_to_str(reservation, seats) + "\n"  # add reservation to return value
    return retval


def get_times(client: socket, data: list[Union[str, int]]) -> str:
    if len(data) != 3:  # data[0] is uuid, data[1] is command, data[2] is title
        return "Invalid Parameters"


def get_seats(client: socket, data: list[Union[str, int]]) -> str:
    if len(data) != 3:  # data[0] is uuid, data[1] is command, data[2] is movie_id
        return "Invalid Parameters"

    seats = SQLHelper.get_seats(data[2])  # get all seats for movie
    retval = ""  # return value
    for i in range(0, 99):  # iterate over possible seats, as all seats aren't prepopulated
        if any(seat["seat_number"] == i for seat in seats): # if seat is reserved
            retval += "1"  # mark seat as reserved
        else:
            retval += "0"  # we can assume it's available
        retval += "::"  # add delimiter

    return retval
