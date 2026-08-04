import socket


SERVER_PORT = 5678

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost', SERVER_PORT))

while True:
    command = input("NymeriaDB> ")

    server.sendall(command.encode())
    if command.lower() == "exit" or command.lower() == "shutdown":
        server.close()
        break   
    print(server.recv(1024).decode())
