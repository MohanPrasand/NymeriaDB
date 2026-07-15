import os
from lsm_tree import lsm_tree
import pickle

print("loading db...")

if os.path.exists("./data/lsm.bin"):
    lsm = pickle.load(open("./data/lsm.bin", "rb"))
else:
    lsm = lsm_tree.LSM_Tree()

while True:
    print("Choose:\n1. insert key, val\n2. delete key\n3. get key\nEnter choice: ", end="")
    ch = int(input())
    if ch == 1:
        key, val = input("key: "), input("val: ")
        lsm.insert(key, val)
        print(f"inserted {key}, {val}")

    elif ch == 2:
        key = input("key: ")
        lsm.delete(key)
        print(f"deleted {key}")
    
    elif ch == 3:
        key = input("key: ")
        print(lsm.search(key))

    else:
        break

print("shutting down db...")
pickle.dump(lsm, open("./data/lsm.bin", "wb"))
