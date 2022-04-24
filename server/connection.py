import sqlite3
from socket import socket

import commands
from consts import Errors
import consts


class Client:
    # noinspection PyTypeChecker
    def __init__(self, connection: socket, address: tuple) -> None:
        self.connection = connection
        self.address = address
        self.uuid: str = None
        self.active: bool = True
        self.user: sqlite3.Row = None

    def listen(self) -> None:
        while self.active:
            data: bytes = self.connection.recv(consts.SOCKET_BUFFER_SIZE)
            if not data:
                self.connection.close()

            print(data.decode("utf-8"))
            resp: str = parse_data(self, data)
            if resp is None:
                resp = Errors.NO_RESPONSE
            elif resp == "":
                resp = Errors.EMPTY_RESPONSE
            while resp[-1] == ":" or resp[-1] == '\n':  # remove trailing colons, newlines
                resp = resp[:-1]
            try:
                self.connection.send(str(resp).encode("utf-8"))
            except OSError:
                self.active = False
        self.connection.close()
        print(f"Disconnected from {self.address}")


def new_client(conn: socket, addr: tuple) -> None:
    """
    Creates a new client and starts listening for data from the client.
    :param conn: the connection to the client
    :param addr: the address of the client
    :return: None
    """
    client = Client(conn, addr)
    client.listen()


def parse_data(client: Client, data: bytes) -> str:
    """
    Parses the data received from the client and returns the response to be sent.
    :param client: the client that sent the data
    :param data: the data received from the client
    :return: response to be sent to the client
    """

    if len(data) == 0:  # if no data was received
        client.active = False  # close the connection, client is dead
        return Errors.CONN_CLOSED

    if client.uuid is None:
        client.uuid = data.split()[0].decode("utf-8")
    data = data.decode("utf-8")
    data = data.split("::")
    if data[1] == "":  # if the command is empty, return an error
        return Errors.NO_INPUT

    # data[0] will always be uuid after login
    # data[1] will always be the command

    if data[1] == "register":
        return commands.register(client, data)

    elif data[1] == "reserve":
        return commands.reserve(client, data)

    elif data[1] == "get_unique_movies":
        return commands.get_unique_movies(client, data)

    elif data[1] == "get_reservations":
        return commands.get_reservations(client, data)

    elif data[1] == "get_movies":
        return commands.get_movies(client, data)

    elif data[1] == "get_seats":
        return commands.get_seats(client, data)

    elif data[1] == "create_movie":
        return commands.create_movie(client, data)

    elif data[1] == "get_times":
        return commands.get_times(client, data)

    elif data[1] == "get_dates":
        return commands.get_dates(client, data)

    elif data[1] == "get_theaters":
        return commands.get_theaters(client, data)

    return Errors.INVALID_COMMAND
