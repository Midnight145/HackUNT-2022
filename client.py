import socket
import hashlib
import os
import sys
import json

with open("uuid.dat", "w+") as f:
    uuid_ = f.read()


def parse_command(x):
    return x.split(" ")


PORT = 31337
HOST = "127.0.0.1"
login = False
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:
        try:
            data = sock.recv(1024)
            if login and not uuid_:
                with open("uuid.dat", "w+") as f:
                    f.write(data.decode())
                    uuid_ = data.decode()
                login = False
            if not data:
                break
            print(data.decode())
            sendval = input("Enter a message: ")
            ret = parse_command(sendval)
            if ret[0] == "login":
                login = True
            else:
                sendval = uuid_ + " " + sendval
            sock.send(sendval.encode())
        except KeyboardInterrupt:
            sock.close()
            sys.exit()
