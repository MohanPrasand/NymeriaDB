import os

class WAL:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
        self.file = open(path, "a+")
        self.file.seek(0, 2)

    def log(self, *vals):
        self.file.write(",".join(vals) + "\n")
        self.file.flush()

    def replay(self):
        self.file.seek(0)
        for line in self.file:
            vals = line.strip().split(",")
            yield tuple(vals)

    def rotate(self):
        self.file.close()
        os.rename(self.path, self.path + ".old")
        self.file = open(self.path, "a+")
        self.file.seek(0, 2)

    def clear(self):
        self.file.close()
        os.remove(self.path)
        self.file = open(self.path, "a+")
        self.file.seek(0, 2)

    def close(self):
        self.file.close()