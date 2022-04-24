# Server Spec

## Passing Commands

- Commands will be passed in the format of `uuid::command::param1::param2::...`
- Likewise, responses will be passed in a '::' delimited format, as outlined below

## Commands

- ### reserve
  - Creates a movie reservation and adds it to the database
  - Parameters: date, time, theater, movie_id, seats+
    - Seats are added at the end of the command, each being its own parameter
    - The command will be passed to the server as `uuid::reserve::date::time::theater::movie_id::seats1::seats2::...`
  - Example: `uuid::reserve::20220424::1030::1::1::2::3`
  - Response: `uuid::reserve::success::reservation_id`

- ### get_unique_movies
  - Returns a list of all unique movies titles in the database
  - Parameters: none
  - Example: `uuid::get_unique_movies`
  - Response: `title1::title2::...`

- ### get_reservations
  - Returns a `\n`-delimited list of all reservations assigned to the current UUID in the database
  - Parameters: none
  - Example: `uuid::get_reservations`
  - Response:
```
reservation_id::date::time::theater::movie_id::seats1::seats2::...
reservation_id::date::time::theater::movie_id::seats1::seats2::...
```
- ### get_movies
  - Returns a `\n`-delimited list of all movies in the database
  - Parameters: none
  - Example: `uuid::get_movies`
  - Response:
```
movie_id::title::rating::time::date::theater::seats_available::capacity
movie_id::title::rating::time::date::theater::seats_available::capacity
```
- ### get_seats
  - Returns the reserved status of all seats in a movie, where 1 is reserved and 0 is available
  - Parameters: movie_id
  - Example: `uuid::get_seats::1`
  - Response: `seat1_status::seat2_status::...`