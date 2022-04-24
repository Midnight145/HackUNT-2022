import shlex
import sqlite3
from socket import socket

import commands


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
            data: bytes = self.connection.recv(1024)
            if not data:
                self.connection.close()

            print(data.decode("utf-8"))
            resp: str = parse_data(self, data)
            if resp is not None:
                self.connection.send(str(resp).encode("utf-8"))
            else:
                self.connection.send(b"ERROR")


def new_client(conn: socket, addr: tuple) -> None:
    client = Client(conn, addr)
    client.listen()


def parse_data(client: Client, data: bytes) -> str:
    if client.uuid is None:
        client.uuid = data.split()[0].decode("utf-8")
    data = data.decode("utf-8")
    data = shlex.split(data)
    if len(data) == 1:
        return "Invalid Command"

    # data[0] will always be uuid after login
    # data[1] will always be the command

    if data[1] == "reserve":
        return commands.reserve(client, data)

    elif data[1] == "view":
        pass

    elif data[1] == "create":
        return commands.create(client, data)

    elif data[1] == "get_unique_movies":
        return commands.get_unique_movies(client, data)

    elif data[1] == "get_reservations":
        return commands.get_reservations(client, data)

    return "Invalid Command"
