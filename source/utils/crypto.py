import hashlib

class Crypto:

    def __init__(self, enconding = "utf-8",chunk_size = 64 * 1024):
        self.enconding =  enconding
        self.chunk_size = chunk_size

    def hash(self, data: bytes):
        sha1 = hashlib.sha1(data)
        return sha1.hexdigest()

    def hash_bytes(self, data: bytes):
        sha1 = hashlib.sha1(data)
        return sha1.digest()