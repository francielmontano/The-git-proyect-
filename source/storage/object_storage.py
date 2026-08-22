import fs
from source.utils.crypto import crypto
from pathlib import Path

class Objetos:
    def __init__(self,ruta:str):
        self.fs = fs
        self.crypto = crypto()
        self.ruta = Path(ruta)

    def storage_object(self,obj_data: str, data:bytes):
        header = f"{obj_data} {len(data)}\x00".encode("utf-8")
        header_hash = header + data
        hash = self.crypto.hash(header_hash)
        carpeta_objeto = self.ruta / hash[:2]
        ruta_objeto = carpeta_objeto / hash[2:]

        if self.fs.exists(ruta_objeto):
            return hash
        self.fs.crear_directorio(carpeta_objeto)
        self.fs.escribir_bytes(ruta_objeto, data)
        return hash

    def read_object(self, hash):
        ruta_objeto = self.ruta / hash[:2] / hash[2:]

        if not self.fs.exists(ruta_objeto):
            return None

        data = self.fs.leer_byte(ruta_objeto)
        partes = data.split(b"\x00",1)
        header = partes[0].decode("utf-8")
        tipo_obj = header.split(" ")[0]
        return tipo_obj, partes[1]
    