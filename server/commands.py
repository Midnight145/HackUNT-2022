import uuid

import SQLHelper
import auth

from structs import *


def login(client, data):
    if client.logged_in:
        return "Already logged in"
    if len(data) < 3:
        return "Invalid arguments"
    username = data[1]
    password = ''.join(data[2:])
    user = SQLHelper.get_user_by_name(username)
    print("username:", username)
    print("user:",user)
    if user is None:
        return "User does not exist"
    if auth.verify_password(password, user[3], user[4]):
        client.logged_in = True
        client.uuid = user[0]
        return user[0]
    if not client.logged_in:
        return "Not logged in"


def register(client, data):
    if client.user:
        return "User already exists"
    if len(data) < 4:
        return "Invalid arguments"
    print("Registering user")
    username = data[1]
    user_uuid = str(uuid.uuid4())
    email = data[2]
    password = ''.join(data[3:])
    password, salt = auth.hash_new_password(password)
    print(password, salt)
    SQLHelper.add_user(user_uuid, username, email, password, salt)
    return user_uuid


def reserve(client, data):
    if len(data) < 5:
        return "Invalid Parameters"
    if data[2] == "seat":
        return SeatReservation(data[0], data[3], data[4], data[5])
    elif data[2] == "movie":
        return MovieReservation(data[0], data[3], data[4], ' '.join(data[5:]))
    return "Invalid Command"