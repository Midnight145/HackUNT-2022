from typing import Union, TYPE_CHECKING
import shlex
import commands

if TYPE_CHECKING:
    from server.structs import MovieReservation, SeatReservation


class Client:
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        self.uuid = None
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
    if client.uuid is None:
        client.uuid = data.split()[0].decode("utf-8")
    data = data.decode("utf-8")
    data = shlex.split(data)
    if len(data) == 1:
        return "Invalid Command"

    # data[0] will always be uuid after login
    if data[1] == "reserve":
        return commands.reserve(client, data)

    elif data[1] == "view":
        pass

    elif data[1] == "create":
        return commands.create(client, data)

    elif data[1] == "get_movies":
        return commands.get_movies(client, data)

    elif data[1] == "get_reservations":
        return commands.get_reservations(client, data)


    return "Invalid Command"
