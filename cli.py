import socket
import sys


def get_named_arg(arg_name):
    for arg in sys.argv:
        if arg.startswith(f"--{arg_name}="):
            return arg.split("=")[1]
    return None

SERVER_PORT = 5678
HOST = get_named_arg("host") or "localhost"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, SERVER_PORT))

while True:
    command = input("NymeriaDB> ")

    server.sendall(command.encode())
    if command.lower() == "exit" or command.lower() == "shutdown":
        server.close()
        break   
    print(server.recv(1024).decode())
