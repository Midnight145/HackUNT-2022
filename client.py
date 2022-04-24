import socket
import hashlib
import os
import sys
import json
import shlex
import uuid

with open("uuid.dat", "w+") as f:
    uuid_ = f.read()


def parse_command(x):
    return shlex.split(x)


PORT = 31338
HOST = "127.0.0.1"
register = False
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:
        try:
            data = sock.recv(1024)
            # if register and not uuid_:
            if not uuid_:
                with open("uuid.dat", "w+") as f:
                    uuid_ = str(uuid.uuid4())
                    f.write(str(uuid_))
                # register = False
            if not data:
                break
            print(data.decode())
            sendval = input("Enter a message: ")
            print(sendval)
            ret = parse_command(sendval)
            # if ret[0] == "register":
            #     register = True
            # else:
            print(uuid_)
            sendval = uuid_ + " " + sendval
            sock.send(sendval.encode())
        except KeyboardInterrupt:
            sock.close()
            sys.exit()
