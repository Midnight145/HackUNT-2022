import uuid

import SQLHelper
import auth
# from server import structs


# def login(client, data):
#
#     user = SQLHelper.get_user_by_uuid(data[0])
#     if user is None:
#         SQLHelper.add_user(data[0], data[1], data[2])
#         user = SQLHelper.get_user_by_uuid(data[0])
#     client.user = user
#     client.uuid = data[0]
#     return "Logged in: " + data[0]


def reserve(client, data):
    if len(data) < 7:
        return "Invalid Parameters"
    uuid_ = data[0]
    command = data[1]
    date = data[2]
    time = data[3]
    theater = data[4]
    seats = data[5]
    movie_id = data[6]
    print("Reserving seats")

    user = SQLHelper.get_user_by_uuid(client.uuid)
    movie = SQLHelper.get_movie_by_id(movie_id)
    theater = SQLHelper.get_theater_by_name(theater)
    movie_seats = [i for i in movie["seats"]]
    seats = [i for i in seats]
    occupied = []
    if any(i in movie_seats for i in seats):
        return "Invalid seats"

    if movie is None:
        return f"Movie with id {movie_id} not found"

    if movie["rating"] == "R" or movie["rating" == "NC-17"] and user["age"] < 18:
        return "You are too young to reserve this movie"

    bitmask = 0b01111111
    movie_seat_positions = [i & bitmask for i in movie["seats"]]
    seat_positions = [i & bitmask for i in seats]
    for i in seat_positions:
        if i > 99:
            return "Invalid seats"
        movie_seats[movie_seat_positions.index(i)] = seats[i]
    available_seats = [i for i in seats if i <= 99]
    SQLHelper.update_movie_seats(movie_id, movie_seats)
    SQLHelper.update_movie_availability(movie_id, len(available_seats))

    SQLHelper.add_reservation(uuid_, movie_id, date, time, theater, seats)
    return "Reserved"


def create(client, data):
    uuid = data[0]
    if not SQLHelper.is_admin(uuid):
        return "Permission denied"

    command = data[1]
    tablename = data[2]
    columns = data[3:]

    if tablename == "users":
        SQLHelper.add_user(columns[0], columns[1], columns[2])

    if tablename == "movies":
        SQLHelper.add_movie(columns[0], columns[1], columns[2], columns[3], columns[4])

    if tablename == "theaters":
        SQLHelper.add_theater(columns[0], columns[1], columns[2], columns[3])

    if tablename == "admins":
        SQLHelper.add_admin(columns[0])

    return "Table created"


def execute(client, data):
    if len(data) < 2:
        return "Invalid Parameters"
    uuid = data[0]
    command = data[1]
    if not SQLHelper.is_admin(uuid):
        return "Permission denied"
    SQLHelper.execute(''.join(data[2:]))

    return "Executed"
