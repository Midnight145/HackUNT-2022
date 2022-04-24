from socket import socket
from typing import Union, TYPE_CHECKING
import SQLHelper
from consts import Errors

if TYPE_CHECKING:  # avoid circular import, always false
    from connection import Client


def reserve(client: 'Client', data: list[Union[str, int]]) -> str:
    if len(data) < 4:  # data[0] is uuid, data[1] is command, data[2] is movie_id, data[3] is seats
        return Errors.INVALID_PARAMS
    uuid_ = data[0]
    movie_id = data[2]
    seats = data[3:]  # all seats are this param or later

    print("Reserving seats")

    user = SQLHelper.get_user_by_uuid(client.uuid)
    movie = SQLHelper.get_movie_by_id(movie_id)
    date = movie['date']
    time = movie['time']
    theater_id = movie['theater']
    reserved_seats = SQLHelper.get_reserved_seats(movie_id)

    reserved_seat_numbers = [str(i["seat_number"]) for i in reserved_seats]

    if movie is None:  # movie does not exist
        return Errors.NOT_FOUND

    if any(i in reserved_seat_numbers for i in seats):  # seat is reserved
        return Errors.SEATS_TAKEN

    # check rating
    rating = movie["rating"].lower()
    if rating == "r" or rating == "nc-17" and user["age"] < 18:
        return Errors.PERMISSION_DENIED

    if len(seats) != len(set(seats)):  # duplicate seats
        return Errors.DUP_SEATS

    theater = SQLHelper.get_theater_by_id(theater_id)

    if any(int(i) > theater["capacity"] - 1 or int(i) < 0 for i in seats):  # seat number is out of range
        return Errors.INVALID_SEATS

    SQLHelper.reserve_seats(uuid_, movie_id, data[3:])  # reserve seats

    reserved_seats = SQLHelper.get_reserved_seats(movie_id)  # get reserved seats to get updated seat numbers

    SQLHelper.update_movie_availability(movie_id, theater["capacity"] - len(
        reserved_seats))  # update movie availability-- subtract reserved seats from total seats

    SQLHelper.add_reservation(uuid_, movie_id, date, time, theater)  # add reservation
    reservation_id = SQLHelper.get_reservation(uuid_, movie_id)["id"]  # get reservation to get id

    return f"success::{reservation_id}"


def create_movie(client: 'Client', data: list[Union[str, int]]) -> str:
    uuid = data[0]
    command = data[1]
    title = data[2]
    rating = data[3]
    date = data[4]
    time = data[5]
    theater = data[6]
    seats_available = data[7]
    capacity = data[8]
    if not SQLHelper.is_admin(uuid):
        return Errors.PERMISSION_DENIED
    movie_id = SQLHelper.add_movie(title, rating, date, time, theater, seats_available, capacity)

    return f"success::{movie_id}"


# RESPONSES SENT TO CLIENT

def register(client: 'Client', data: list[Union[str, int]]) -> str:
    if len(data) != 3:
        return Errors.INVALID_PARAMS
    command = data[0]
    name = data[1]
    age = data[2]

    if not age.isdigit():
        return Errors.INVALID_PARAMS
    
    new_uuid = SQLHelper.create_user(name, age)
    return f"success::{new_uuid}"


def get_movies_by_title(client: 'Client', data: list[Union[str, int]]) -> str:

    def movie_to_str(__movie):  # helper function to convert movie to string
        return (
            f"{__movie['id']}::{__movie['title']}::{__movie['rating']}::{__movie['showdate']}::{__movie['showtime']}"
            f"::{__movie['theater']}::{__movie['available']}::{__movie['capacity']}")

    if len(data) != 3:  # data[0] is uuid, data[1] is command, data[2] is title
        return Errors.INVALID_PARAMS
    title = data[2]  # title of movie

    movies = SQLHelper.get_movies_by_title(title)
    retval = ""
    for movie in movies:
        retval += movie_to_str(movie) + "\n"

    return retval


def get_unique_movies(client: 'Client', data: list[Union[str, int]]) -> str:
    if len(data) != 2:  # data[0] is uuid, data[1] is command-- no params
        return Errors.INVALID_PARAMS

    movies = list(SQLHelper.get_unique_movies())  # get all movies
    return '::'.join(movies)  # format for sending to client-- title1::title2::title3


def get_movies(client: 'Client', data: list[Union[str, int]]) -> str:
    if len(data) > 2:  # data[0] is uuid, data[1] is command-- no params
        return Errors.INVALID_PARAMS

    def movie_to_str(__movie):  # helper function to convert movie to string
        return (
            f"{__movie['id']}::{__movie['title']}::{__movie['rating']}::{__movie['showdate']}::{__movie['showtime']}"
            f"::{__movie['theater']}::{__movie['available']}::{__movie['capacity']}")

    movies = SQLHelper.get_movies()  # get all movies
    retval = ""  # return value
    for movie in movies:
        retval += movie_to_str(movie) + "\n"  # add movie to return value
    return retval


def get_reservations(client: 'Client', data: list[Union[str, int]]) -> str:
    if len(data) > 2:  # data[0] is uuid, data[1] is command-- no params
        return Errors.INVALID_PARAMS

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


def get_dates(client: 'Client', data: list[Union[str, int]]) -> str:
    if len(data) != 3:  # data[0] is uuid, data[1] is command, data[2] is title
        return Errors.INVALID_PARAMS

    dates = SQLHelper.get_dates(data[2])  # get dates for movie
    retval = ""
    for date in dates:
        retval += date + "::"
    return retval


def get_times(client: 'Client', data: list[Union[str, int]]) -> str:
    if len(data) != 4:  # data[0] is uuid, data[1] is command, data[2] is title, data[3] is date
        return Errors.INVALID_PARAMS

    times = SQLHelper.get_times(data[2], data[3])  # get times for movie
    retval = ""
    for time in times:
        retval += time + "::"
    return retval


def get_seats(client: 'Client', data: list[Union[str, int]]) -> str:
    if len(data) != 3:  # data[0] is uuid, data[1] is command, data[2] is movie_id
        return Errors.INVALID_PARAMS

    seats = SQLHelper.get_seats(data[2])  # get all seats for movie
    retval = ""  # return value
    for i in range(0, 99):  # iterate over possible seats, as all seats aren't prepopulated
        if any(seat["seat_number"] == i for seat in seats): # if seat is reserved
            retval += "1"  # mark seat as reserved
        else:
            retval += "0"  # we can assume it's available
        retval += "::"  # add delimiter

    return retval


def get_theaters(client: 'Client', data: list[Union[str, int]]) -> str:

    def theater_to_string(theater):
        return f"{theater['id']}::{theater['theater_name']}:{theater['capacity']}"
    theaters = SQLHelper.get_theaters()  # get all theaters
    retval = ""  # return value

    # todo: fix retval

    for theater in theaters:
        retval += theater_to_string(theater) + "\n"  # add theater to return value
    return retval
