from typing import Union, TYPE_CHECKING

import commands

if TYPE_CHECKING:
    from server.structs import MovieReservation, SeatReservation


class Client:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.uuid = None
        self.logged_in = False
        self.active = True
        self.user = None

    def listen(self):
        while self.active:
            data = self.connection.recv(1024)
            if not data:
                self.connection.close()

            print(data.decode("utf-8"))
            parsed = parse_data(self, data)
            if parsed is not None:
                self.connection.send(str(parsed).encode("utf-8"))
            else:
                self.connection.send(b"ERROR")


def new_client(conn, addr):
    client = Client(conn, addr)
    client.listen()


def parse_data(client, data) -> Union['MovieReservation', 'SeatReservation', str, None]:
    data = data.decode("utf-8")
    data = data.split(" ")
    if data[0] == "register":
        return commands.register(client, data)

    if data[0] == "login":
        return commands.login(client, data)

    # data[0] will always be uuid after login
    if data[1] == "reserve":
        return commands.reserve(client, data)

    return "Invalid Command"