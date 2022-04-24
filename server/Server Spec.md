# Server Spec

## Initial Setup

- The server is a TCP server that listens on port `31337`. All user verification is via the UUID stored with the client.
- UUID generation is done on the server, generate your UUID with `register` and store it.

## Passing Commands

- Commands will be passed in the format of `uuid::command::param1::param2::...`
- Likewise, responses will be passed in a '::' delimited format, as outlined below

## Commands

- ### register
  - Registers the user with the server and returns the UUID to be stored with the client.
  - Parameters: name, age
  - Example: `register::John Smith::21`
  - Returns `success::[uuid]`
  - Returns `failure::[reason]`

- ### reserve
  - Creates a movie reservation and adds it to the database
  - Parameters: movie_id, seats+
    - Seats are added at the end of the command, each being its own parameter
    - The command will be passed to the server as `uuid::reserve::movie_id::seats1::seats2::...`
  - Example: `uuid::reserve:::1::1::2::3`
  - Response: `success::reservation_id`
  - Response: `failure::reason`

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
  - Response: `failure::reason`

  - ### get_seats
    - Returns the reserved status of all seats in a movie, where 1 is reserved and 0 is available
    - Parameters: movie_id
    - Example: `uuid::get_seats::1`
    - Response: `seat1_status::seat2_status::...`

  - ### create_movie
    - Creates a new movie entry and adds it to the database
    - Parameters: title, rating, date, time, theater, seats_available, capacity
    - Example: `uuid::create_movie::"Shrek"::"PG"::20220424::1030::1::100::100`
    - Response: `success::movie_id`
    - Response: `failure::reason`

  - ### get_times
    - Returns the times of all movies of a given name, on a given date
    - Parameters: movie_id, date
    - Example: `uuid::get_times::1::20220424`
    - Response: `time1::time2::...`
    - Response: `failure::reason`

  - ### get_dates
    - Returns the dates of all movies of a given name
    - Parameters: movie_id
    - Example: `uuid::get_dates::1`
    - Response: `date1::date2::...`
    - Response: `failure::reason`

  - ### get_theaters
    - Returns `\n`-delimited list about all theaters in the database
    - Parameters: 
    - Example: `uuid::get_theaters`
    - Response: 
```
theater::id::name::capacity
theater::id::name::capacity
```
  - Response: `failure::reason`