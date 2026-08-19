from lsm_tree import lsm_tree
from lsm_tree.wal import WAL
from manifest_handler import Manifest
import threading

DB_PATH = "./databases"

class Database:
    def __init__(self, db_name):
        self.condition = threading.Condition(threading.Lock())
        self.readers = 0
        self.writer = False
        self.waiting_writers = 0


        self.db_name = db_name
        self.lsm = lsm_tree.LSM_Tree()
        self.wal = WAL(f"{DB_PATH}/{db_name}/wal.log")
        self.manifest = Manifest(f"{DB_PATH}/{db_name}/manifest.json")

        self.lsm.ssTables = self.manifest.read()

        for op in self.wal.replay():
            if op[0] == "insert":
                self.lsm.insert(op[1], op[2])
            elif op[0] == "delete":
                self.lsm.delete(op[1])

    def __acquire_read(self):
        with self.condition:
            while self.writer or self.waiting_writers > 0:
                self.condition.wait()
            self.readers += 1

    def __acquire_write(self):
        with self.condition:
            self.waiting_writers += 1
            while self.readers > 0 or self.writer:
                self.condition.wait()
            self.waiting_writers -= 1
            self.writer = True

    def __release_read(self):
        with self.condition:
            self.readers -= 1
            if self.readers == 0:
                self.condition.notify_all()

    def __release_write(self):
        with self.condition:
            self.writer = False
            self.condition.notify_all() 

    def insert(self, key, val):
        self.__acquire_write()
        self.wal.log("insert", key, val)
        is_compacted = self.lsm.insert(key, val)
        if is_compacted:
            self.manifest.write(self.lsm.ssTables)
            self.wal.clear()
        self.__release_write()
        return True

    def delete(self, key):
        self.__acquire_write()
        self.wal.log("delete", key)
        is_compacted = self.lsm.delete(key)
        if is_compacted:
            self.manifest.write(self.lsm.ssTables)
            self.wal.clear()
        self.__release_write()
        return True

    def get(self, key):
        self.__acquire_read()
        result = self.lsm.search(key)
        self.__release_read()
        return result

    def close(self):
        self.wal.close()

if __name__ == "__main__":
    db = Database()
    while True:
        print("Choose:\n1. insert key, val\n2. delete key\n3. get key\nEnter choice: ", end="")
        ch = int(input())
        if ch == 1:
            db.insert(input("key: "), input("val: "))
        elif ch == 2:
            db.delete(input("key: "))
        
        elif ch == 3:
            key = input("key: ")
            print(f"val: {db.get(key)}")

        else:
            break

    print("shutting down db...")