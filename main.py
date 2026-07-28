import os
from lsm_tree import lsm_tree
from lsm_tree.wal import WAL
from manifest_handler import Manifest

WAL_FILE = "./data/wal.log"
MANIFEST_FILE = "./data/manifest.json"

lsm = lsm_tree.LSM_Tree()
wal = WAL(WAL_FILE)
manifest = Manifest(MANIFEST_FILE)

lsm.ssTables = manifest.read()

for op in wal.replay():
    if op[0] == "insert":
        lsm.insert(op[1], op[2])
    elif op[0] == "delete":
        lsm.delete(op[1])


while True:
    print("Choose:\n1. insert key, val\n2. delete key\n3. get key\nEnter choice: ", end="")
    ch = int(input())
    if ch == 1:
        key, val = input("key: "), input("val: ")
        wal.log("insert", key, val)
        is_compacted= lsm.insert(key, val)
        if is_compacted:
            manifest.write(lsm.ssTables)
            wal.clear()
        print(f"inserted {key}, {val}")

    elif ch == 2:
        key = input("key: ")
        wal.log("delete", key)
        is_compacted = lsm.delete(key)
        if is_compacted:
            manifest.write(lsm.ssTables)
            wal.clear()
        print(f"deleted {key}")
    
    elif ch == 3:
        key = input("key: ")
        print(lsm.search(key))

    else:
        break

print("shutting down db...")