class MovieReservation:
    def __init__(self, uuid_, theater, time, movie):
        # todo: add to database
        self.uuid = uuid_
        self.theater = theater
        self.time = time
        self.movie = movie

    def __str__(self):
        return "UUID: " + self.uuid + " Theater: " + self.theater + " Time: " + self.time + " Movie: " + self.movie


class SeatReservation:
    def __init__(self, uuid_, seat, theater, time):
        # todo: add to database
        self.uuid = uuid_
        self.theater = theater
        self.time = time
        self.seat = seat


class Seat:
    def __init__(self, location=None, row=None, col=None, reserved=False):
        self.row = row
        self.col = col
        self.reserved = reserved
        self.location = location

    @staticmethod
    def from_int(seat_int):
        reserved_mask = 0b10000000
        reserved = seat_int & reserved_mask
        location_mask = 0b01111111
        location = seat_int & location_mask
        row = location // 10
        col = location % 10
        return Seat(location, row, col, reserved)

    # todo: test
    def to_int(self):
        reserved_mask = 0b10000000
        retval = self.reserved & reserved_mask
        retval += self.location
        return retval
