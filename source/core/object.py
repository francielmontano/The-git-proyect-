from utils.crypto import Crypto
class GitObject:

    def __init__(self):
        self._crypto = Crypto()

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
    def __init__(self, content: bytes):
        self.content = content

    @property
    def type_name(self):
        return "blob"

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

{self.message}"""
        return texto.encode("utf-8")

    def deserialize(self, data):
        text = data.decode("utf-8")
        header_part, self.message = text.split("\n\n", 1)
    
        for line in header_part.splitlines():
            if line.startswith("tree "):
                self.tree_hash = line.split(" ", 1)[1]
            elif line.startswith("parent "):
                self.parent_hash = line.split(" ", 1)[1]
            elif line.startswith("author "):
                self.author = line.split(" ", 1)[1]
        return self

class Tree(GitObject):
    def __init__(self, entries=None):
        self.entries = entries if entries is not None else []
        self._crypto = Crypto()

    @property
    def type_name(self):
        return "tree"

    def add_entry(self, path, sha):
        self.entries.append((path, sha))

    def serialize(self):
        # Ordenamos las entradas por su ruta
        sorted_entries = sorted(self.entries, key=lambda entry: entry[0])
        result = []
        for path, sha in sorted_entries:
            # Guardamos la ruta y el hash separados por un espacio
            result.append(f"{path} {sha}")
        
        # Unimos todo con saltos de línea y lo convertimos a bytes legibles (UTF-8)
        return "\n".join(result).encode("utf-8")

    def deserialize(self, data):
        self.entries = []
        if not data:
            return self
            
        # Decodificamos el texto y lo separamos línea por línea
        lineas = data.decode("utf-8").split("\n")
        for linea in lineas:
            if linea.strip(): # Evitamos líneas vacías
                path, sha_hex = linea.split(" ", 1)
                self.entries.append((path, sha_hex))
        return self