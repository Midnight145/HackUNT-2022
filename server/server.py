import socket
import threading

import SQLHelper
import connection

PORT = 31337
HOST = "127.0.0.1"
DB_FILE = "server.db"

clients = []


SQLHelper.init()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Listening on port " + str(PORT))
    print("Waiting for connections")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=connection.new_client, args=(conn, addr), daemon=True).start()
        print(type(addr))

        print("Connected to: ", addr)
        conn.send(b"Hello, client!")
