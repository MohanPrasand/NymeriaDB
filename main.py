import socket
from database import Database


DB = None
PORT = 5678

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', PORT))
server.listen(5)

def execute_command(command):
    command[0] = command[0].lower()
    if command[0] == "select":
        if len(command) != 2:
            return "Error: select command requires database name"
        db_name = command[1]
        global DB
        DB = Database(db_name)
        return f"Database selected: {db_name}"

    if not DB:
        return "Error: No database selected. Use 'select <db_name>' to select a database."
    
    if command[0] == "insert":
        if len(command) != 3:
            return "Error: insert command requires key and value"
        key, val = command[1], command[2]
        DB.insert(key, val)
        return f"Inserted key: {key}, value: {val}"
    elif command[0] == "delete":
        if len(command) != 2:
            return "Error: delete command requires key"
        key = command[1]
        DB.delete(key)
        return f"Deleted key: {key}"
    elif command[0] == "get":
        if len(command) != 2:
            return "Error: get command requires key"
        key = command[1]
        val = DB.get(key)
        return f"Value for key {key}: {val}"
    elif command[0] == "shutdown":
        return "Shutting down DB..."
    else:
        return "Error: Unknown command"

while True:
    conn, addr = server.accept()
    print(f"Connection from {addr} has been established!")
    SHUTDOWN = False
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        command = data.strip().split()
        execution_result = execute_command(command)+"\n"
        conn.sendall(execution_result.encode())
        if command[0].lower() == "shutdown":
            SHUTDOWN = True
            break
    conn.close()
    if SHUTDOWN:
        break