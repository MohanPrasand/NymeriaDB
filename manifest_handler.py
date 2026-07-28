import json
from lsm_tree.bloom_filter import BloomFilter
import os

class Manifest:
    def __init__(self, filepath):
        self.filepath = filepath
        if not os.path.exists(filepath):
            with open(filepath, 'w') as f:
                json.dump({"tables": []}, f)

    def write(self, ss_tables):
        data = {"tables": []}
        for i in range(len(ss_tables)):
            for ss_table in ss_tables[i]:
                c = {"level": i, "start": ss_table["start"], "end": ss_table["end"], "file": ss_table["file"], "bloom_filter": ss_table["bloom_filter"].bits}
                data["tables"].append(c)

        with open(self.filepath, 'w') as f:
            json.dump(data, f)

    def read(self):
        data = None
        with open(self.filepath, 'r') as f:
            data = json.load(f)

        if not data["tables"]:
            return [[], [], []]

        ss_tables = []
        for i in range(max([t["level"] for t in data["tables"]]) + 1):
            ss_tables.append([])

        if not ss_tables:
            return ss_tables

        for t in data["tables"]:
            ss_tables[t["level"]].append({
                "start": t["start"],
                "end": t["end"],
                "file": t["file"],
                "bloom_filter": BloomFilter(size=1024, bits=t["bloom_filter"])
            })

        return ss_tables