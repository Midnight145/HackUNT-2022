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
        try:
            conn, addr = s.accept()
        except KeyboardInterrupt:
            print("\nShutting down server...")
            for client in clients:
                client.close()
            s.close()
            print("Server shut down.")
            exit(0)
        threading.Thread(target=connection.new_client, args=(conn, addr), daemon=True).start()

        print("Connected to: ", addr)
        conn.send(b"Hello, client!")
