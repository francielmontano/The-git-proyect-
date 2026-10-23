from storage import fs
from .ref import Head
from .index import Index
from .object import Blob, Commit, Tree
from utils.crypto import Crypto
from storage.object_storage import Objetos
from pathlib import Path
from storage.reparar import restaurar
class Repository:
    def __init__(self, ruta=".minigit", rama="main"):
        self.ruta = Path(ruta)
        self.rama = rama
        self.ref = Head(Path(self.ruta / "refs" / "heads" / self.rama))
        self._index = Index(self.ruta)
        self.objeto = Objetos(self.ruta / "objects")

    def init(self):
        if not fs.exists(self.ruta):
            fs.crear_directorio(self.ruta)
            fs.crear_directorio(self.ruta / "objects")
            fs.crear_directorio(self.ref.git_dir, True)
        return "El repositorio ha sido inicializado con exito!"

    def add(self, file):
        # Corregida la estructura condicional para que no retorne el error siempre
        if fs.exists(self.ruta):
            self._index.add(file)
            return "OK"
        else:
            return "Error: No existe un repositorio iniciado: minigit init"

    def commit(self, author, message: str):
        self._index.load() 
        tree = Tree()
        def recursive(archivo_o_carpeta):
            ruta = Path(archivo_o_carpeta)
            contenido = fs.listar_contenido(ruta)
            if isinstance(contenido, list):
                for element in contenido:
                    recursive(element)
                return
            bytes_file = fs.leer_byte(ruta) 
            
            if bytes_file is not None:
                blob = Blob(bytes_file)
                hash_file = self.objeto.storage_object(blob.type_name, blob.content)
                tree.add_entry(archivo_o_carpeta, hash_file)
            else:
                print(f"No se pudo leer el archivo en: {ruta.resolve()}")

        for file in self._index.entries:
            recursive(file)
            
        hash_tree = self.objeto.storage_object(tree.type_name, tree.serialize())
        parent = fs.leer_byte(self.ref.git_dir)
        commit = Commit(hash_tree, parent.decode("utf-8"), author, message)
        hash_commit = self.objeto.storage_object(commit.type_name, commit.serialize())
        self.ref.write_head(hash_commit)
        self._index.clear()

    def log(self):
        parent_commit = fs.leer_byte(self.ref.git_dir)
        parent_commit.decode("utf-8")
        while parent_commit != "":
            parent = self.objeto.read_object(parent_commit)
            contenido_texto = parent[1].decode('utf-8')
            for linea in contenido_texto.splitlines():
                if linea.startswith("parent "):
                    parent_hash = linea.split(" ")[1]
                    break
            yield contenido_texto
            parent_commit = parent_hash

    def remove(self, file):
        """Remueve un archivo específico del staging."""
        if fs.exists(self.ruta):
            self._index.remove(file)

    def clear_index(self):
        """Vacía todo el staging."""
        if fs.exists(self.ruta):
            self._index.clear()

    def restorage(self,tree):
        """Restaura los objetos blob a su archivo original"""
        carpeta_ruta = tree[:2]
        ruta = tree[2:]
        ruta_pricipal = Path(self.ruta / "objects")
        tree_ruta= fs.leer_byte(ruta_pricipal / carpeta_ruta / ruta).decode("utf-8")

        for linea in tree_ruta.splitlines():
            archivo_nombre, hash_commit = linea.rsplit(' ', 1)
            carpeta_archivo = hash_commit[:2]
            ruta_archivo = hash_commit[2:]
            restaurar(Path(ruta_pricipal / (carpeta_archivo) / ruta_archivo), archivo_nombre)