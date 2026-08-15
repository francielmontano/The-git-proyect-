import hashlib
from pathlib import Path
from typing import List, Optional


class GitTreeManager:
    """
    Gestiona el cálculo recursivo de hashes SHA-1 para archivos (blobs) 
    y directorios (trees) utilizando una sola clase estructurada.
    """

    def __init__(self, ruta: Path,chunk_size = 64 * 1024):
        self.ruta = Path(ruta)
        self.nombre = self.ruta.name
        self.chunk_size = chunk_size

    def _calcular_hash_archivo(self, ruta_archivo: Path) -> Optional[str]:
        """Calcula el hash SHA-1 de un archivo leyendo por bloques en streaming."""
        if not ruta_archivo.is_file():
            return None

        sha1 = hashlib.sha1()
        try:
            with open(ruta_archivo, "rb") as f:
                while chunk := f.read(self.chunk_size):
                    sha1.update(chunk)
            return sha1.hexdigest()
        except (FileNotFoundError, PermissionError):
            return None

    def _formatear_entrada_archivo(self, ruta_archivo: Path) -> Optional[str]:
        """Genera la línea formateada 'blob <hash> <nombre>' para un archivo."""
        hash_blob = self._calcular_hash_archivo(ruta_archivo)
        if hash_blob:
            return f"blob {hash_blob} {ruta_archivo.name}\n"
        return None

    def _obtener_entradas_directorio(self) -> List[str]:
        """
        Escanea el directorio de forma recursiva, procesando archivos (blobs) 
        y subdirectorios (trees) mediante nuevas instancias de la clase.
        """
        if not self.ruta.exists() or not self.ruta.is_dir():
            return []

        entradas: List[str] = []

        # Ordenar elementos alfabéticamente ignorando mayúsculas/minúsculas
        elementos_ordenados = sorted(
            self.ruta.iterdir(), key=lambda x: x.name.lower()
        )

        for elemento in elementos_ordenados:
            if elemento.is_dir():
                # Procesamiento recursivo: se crea una subinstancia para la subcarpeta
                sub_gestor = GitTreeManager(elemento)
                sub_hash = sub_gestor.calcular_hash()
                if sub_hash:
                    entradas.append(f"tree {sub_hash} {elemento.name}\n")

            elif elemento.is_file():
                # Procesamiento de archivo individual
                linea_blob = self._formatear_entrada_archivo(elemento)
                if linea_blob:
                    entradas.append(linea_blob)

        return entradas

    def calcular_hash(self) -> Optional[str]:
        """
        Calcula el hash SHA-1 definitivo del directorio procesando todas sus entradas.
        """
        entradas = self._obtener_entradas_directorio()
        if not entradas:
            return None

        # Ordenamiento determinista de las entradas
        entradas.sort()

        # Ensamblado del contenido en bytes
        contenido_plano = "".join(entradas)
        data_bytes = contenido_plano.encode("utf-8")

        # Generación del hash global SHA-1
        motor = hashlib.sha1()
        motor.update(data_bytes)
        return motor.hexdigest()
