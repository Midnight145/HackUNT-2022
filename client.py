import socket
import sys
import uuid

with open("uuid.dat", "r") as f:
    uuid_ = f.read()


def parse_command(x):
    return x.split("::")


PORT = 31337
HOST = "127.0.0.1"
register = False
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    while True:
        try:
            data = sock.recv(1024)

            if not uuid_:
                with open("uuid.dat", "w+") as f:
                    uuid_ = str(uuid.uuid4())
                    f.write(str(uuid_))
                register = False
            if not data:
                break
            print(data.decode())
            sendval = input("Enter a message: ")
            ret = parse_command(sendval)
            sendval = uuid_ + "::" + sendval
            sock.send(sendval.encode())
        except KeyboardInterrupt:
            print("\nExiting...")
            sock.close()
            sys.exit()
