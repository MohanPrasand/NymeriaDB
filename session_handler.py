from database import Database
from db_assigner import DBAssigner

class SessionHandler:
    def __init__(self):
        self.DB = None

    def execute(self, command):
        return self.__execute_command(command.strip().split())

    def __execute_command(self, command):
        command[0] = command[0].lower()
        if command[0] == "select":
            if len(command) != 2:
                return "Error: select command requires database name"
            db_name = command[1]
            self.DB = DBAssigner().get_db(db_name)
            return f"Database selected: {db_name}"

        if not self.DB:
            return "Error: No database selected. Use 'select <db_name>' to select a database."
        
        if command[0] == "insert":
            if len(command) != 3:
                return "Error: insert command requires key and value"
            key, val = command[1], command[2]
            self.DB.insert(key, val)
            return f"Inserted key: {key}, value: {val}"
        elif command[0] == "delete":
            if len(command) != 2:
                return "Error: delete command requires key"
            key = command[1]
            self.DB.delete(key)
            return f"Deleted key: {key}"
        elif command[0] == "get":
            if len(command) != 2:
                return "Error: get command requires key"
            key = command[1]
            val = self.DB.get(key)
            return f"Value for key {key}: {val}"
        elif command[0] == "shutdown":
            return "Shutting down DB..."
        else:
            return "Error: Unknown command"

if __name__ == "__main__":
    session_handler = SessionHandler()
    while True:
        command = input("Enter command: ")
        if command.lower() == "exit":
            print("Exiting...")
            break
        response = session_handler.execute(command)
        print(response)
