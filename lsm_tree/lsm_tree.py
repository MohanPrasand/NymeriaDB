import os
from . import avl_tree
from . import ss_table


TOMBSTONE = "*del"


class LSM_Tree:

    MAX_MEMTABLE = 10

    def __init__(self):
        self.memTable = None
        self.memTablec = 0

        self.ssTables = [[], [], []]

        self.count = 0

        self.start = None
        self.end = None

    def insert(self, key, val):

        self.memTable = avl_tree.insert(self.memTable, key, val)

        self.start = min(self.start, key) if self.start is not None else key
        self.end = max(self.end, key) if self.end is not None else key

        self.memTablec += 1

        if self.memTablec >= self.MAX_MEMTABLE:

            self.flushMem(self.memTable)

            self.memTable = None
            self.memTablec = 0
            self.start = None
            self.end = None

        return True

    def delete(self, key):

        self.memTable = avl_tree.insert(self.memTable, key, TOMBSTONE)

        self.start = min(self.start, key) if self.start is not None else key
        self.end = max(self.end, key) if self.end is not None else key

        self.memTablec += 1

        if self.memTablec >= self.MAX_MEMTABLE:

            self.flushMem(self.memTable)

            self.memTable = None
            self.memTablec = 0
            self.start = None
            self.end = None

        return True

    def flushMem(self, tree, level=0):

        filepath = f"./data/sstab{self.count}.table"
        self.count += 1

        ss_table.save(tree, filepath)

        self.ssTables[level].append({
            "start": self.start,
            "end": self.end,
            "file": filepath
        })

        if len(self.ssTables[level]) >= 4 * (level + 1):
            self.compact(level)

    def compact(self, level):

        if level >= len(self.ssTables) - 1:
            return

        merged = None

        start = None
        end = None

        old_tables = self.ssTables[level]

        for tb in old_tables:

            start = min(start, tb["start"]) if start is not None else tb["start"]
            end = max(end, tb["end"]) if end is not None else tb["end"]

            tree = ss_table.load(tb["file"])

            for key, value in tree:
                merged = avl_tree.insert(merged, key, value)

        # delete old SSTables
        for tb in old_tables:
            if os.path.exists(tb["file"]):
                os.remove(tb["file"])

        self.ssTables[level] = []

        # reuse flushMem()
        self.start = start
        self.end = end

        self.flushMem(merged, level + 1)

        self.start = None
        self.end = None

    def search(self, key):

        t = self.memTable

        while t:

            if t.key == key:

                if t.val == TOMBSTONE:
                    return None

                return t.val

            elif key < t.key:
                t = t.left

            else:
                t = t.right

        for level in self.ssTables:

            for tb in reversed(level):

                if tb["start"] <= key <= tb["end"]:

                    value = ss_table.search(tb["file"], key)

                    if value is None:
                        continue

                    if value == TOMBSTONE:
                        return None

                    return value

        return None