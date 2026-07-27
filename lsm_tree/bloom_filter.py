import hashlib


class BloomFilter:
    def __init__(self, size=1024):
        self.size = size
        self.bits = 0

    def _hashes(self, key):
        h1 = int(hashlib.md5(key.encode()).hexdigest(), 16) % self.size
        h2 = int(hashlib.sha1(key.encode()).hexdigest(), 16) % self.size
        h3 = int(hashlib.sha256(key.encode()).hexdigest(), 16) % self.size
        return h1, h2, h3

    def add(self, key):
        for h in self._hashes(key):
            self.bits |= (1 << h)

    def contains(self, key):
        for h in self._hashes(key):
            if (self.bits & (1 << h)) == 0:
                return False
        return True
    
    def merge(self, other):
        if self.size != other.size:
            raise ValueError("Bloom filters must be of the same size to merge.")
        self.bits |= other.bits