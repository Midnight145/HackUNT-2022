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