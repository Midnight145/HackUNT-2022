class Errors:
    INVALID_PARAMS = "failure::invalid_params"
    PERMISSION_DENIED = "failure::permission_denied"
    DUP_SEATS = "failure::dup_seats"
    SEATS_TAKEN = "failure::seats_taken"
    INVALID_SEATS = "failure::invalid_seats"
    NOT_FOUND = "failure::not_found"
    INVALID_COMMAND = "failure::invalid_command"
    NO_RESPONSE = "failure::no_response"
    EMPTY_RESPONSE = "failure::empty_response"
    NO_INPUT = "failure::no_input"
    CONN_CLOSED = "failure::conn_closed"

SOCKET_BUFFER_SIZE = 8192