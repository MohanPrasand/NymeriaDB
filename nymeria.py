import socket
import threading
from session_handler import SessionHandler 

HOST = "0.0.0.0"
PORT = 5678

def handle_client(conn, addr):
    print(f"Connected: {addr}")

    handler = SessionHandler()

    try:
        while True:
            data = conn.recv(1024).decode()

            if not data:
                break

            response = handler.execute(data)
            conn.sendall((response + "\n").encode())
    finally:
        conn.close()
        handler.close()
        print(f"Disconnected: {addr}")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"NymeriaDB running on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    thread = threading.Thread(
        target=handle_client,
        args=(conn, addr)
    )

    thread.start()