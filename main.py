import os
from lsm_tree import lsm_tree
from lsm_tree.wal import WAL

WAL_FILE = "./data/wal.log"

lsm = lsm_tree.LSM_Tree()
wal = WAL(WAL_FILE)

for op, *val in wal.replay():
    if op == "insert":
        lsm.insert(*val)
    elif op == "delete":
        lsm.delete(val[0])



while True:
    print("Choose:\n1. insert key, val\n2. delete key\n3. get key\nEnter choice: ", end="")
    ch = int(input())
    if ch == 1:
        key, val = input("key: "), input("val: ")
        wal.log("insert", key, val)
        lsm.insert(key, val)
        print(f"inserted {key}, {val}")

    elif ch == 2:
        key = input("key: ")
        wal.log("delete", key)
        lsm.delete(key)
        print(f"deleted {key}")
    
    elif ch == 3:
        key = input("key: ")
        print(lsm.search(key))

    else:
        break

print("shutting down db...")