import os

class WAL:
    def __init__(self, path):
        self.path = path
        self.file = open(path, "a+")
        self.file.seek(0, 2)

    def log(self, *vals):
        self.file.write(",".join(vals) + "\n")
        self.file.flush()

    def replay(self):
        self.file.seek(0)
        logs = []
        for line in self.file:
            vals = line.strip().split(",")
            logs.append(tuple(vals))
        return logs

    def rotate(self):
        self.file.close()
        os.rename(self.path, self.path + ".old")
        self.file = open(self.path, "a+")
        self.file.seek(0, 2)
