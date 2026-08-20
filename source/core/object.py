from utils.crypto import crypto

class GitObject:

    def __init__(self):
        self._crypto = crypto()

    @property
    def type_name(self):
        """Devuelve el tipo de objeto en texto ('blob', 'tree', 'commit')."""
        pass

    def serialize(self):
        """Devuelve los datos internos del objeto codificados en bytes."""
        pass

    def deserialize(self, data):
        """Reconstruye los atributos del objeto a partir de sus bytes."""
        pass

class Blob(GitObject):
    def __init__(self, content=b""):
        self.content = content

    @property
    def type_name(self):
        return "blob"

    def serialize(self):
        return self.content

    def deserialize(self, data):
        self.content = data

class Commit(GitObject):
    """Representa una instantánea en la historia del proyecto."""

    def __init__(
        self,
        tree_hash="",
        parent_hash=None,
        author="",
        message="",
    ):
        self.tree_hash = tree_hash
        self.parent_hash = parent_hash
        self.author = author
        self.message = message

    @property
    def type_name(self):
        return "commit"

    def serialize(self):
        texto = f"""tree {self.tree_hash}
        parent {self.parent_hash}
        author {self.author}
        
        {self.message}
        """
        return texto.encode("utf-8")

    def deserialize(self, data):
        text = data.decode("utf-8")
        header_part, self.message = text.split("\n\n", 1)
    
        self.parent_hash = None
        for line in header_part.splitlines():
            if line.startswith("tree "):
                self.tree_hash = line.split(" ", 1)[1]
            elif line.startswith("parent "):
                self.parent_hash = line.split(" ", 1)[1]
            elif line.startswith("author "):
                self.author = line.split(" ", 1)[1]

class Tree(GitObject):
    def __init__(self, entries=None):
        self.entries = entries if entries is not None else []
        self._crypto = crypto()
    @property
    def type_name(self):
        return "tree"

    def add_entry(self, mode, path, sha):
        self.entries.append((mode, path, sha))

    def serialize(self):
        sorted_entries = sorted(self.entries, key=lambda entry: entry[1])
        result = bytearray()
        for mode, path, sha in sorted_entries:
            header = f"{mode} {path}\x00".encode("utf-8")
            sha_bytes = bytes.fromhex(sha)
            result.extend(header + sha_bytes)
        return bytes(result)

    def deserialize(self, data):
        self.entries = []
        idx = 0
        total_len = len(data)

        while idx < total_len:
            null_idx = data.index(b"\x00", idx)

            header = data[idx:null_idx].decode("utf-8")
            mode, path = header.split(" ", 1)

            sha_bytes = data[null_idx + 1 : null_idx + 21]
            sha_hex = sha_bytes.hex()

            self.entries.append((mode, path, sha_hex))
            idx = null_idx + 21