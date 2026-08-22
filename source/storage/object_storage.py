from . import fs
from utils.crypto import Crypto
from pathlib import Path

class Objetos:
    def __init__(self,ruta:str):
        self.fs = fs
        self.crypto = Crypto()
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
        hash_texto = hash.decode('utf-8') if isinstance(hash, bytes) else hash
        ruta_objeto = Path(self.ruta / hash_texto[:2] / hash_texto[2:])
    
        if not self.fs.exists(ruta_objeto):
            return None
    
        # 1. Leemos los bytes originales del archivo de forma intacta
        data = self.fs.leer_byte(ruta_objeto)
        texto = data.decode('utf-8')
        
        lineas = texto.splitlines()
        if not lineas:
            print(f"⚠️ ERROR: El objeto {hash_texto} está vacío.")
            return None
    
        # 2. Identificación dinámica del tipo de objeto sin recortar la data
        primera_linea = lineas[0]
        
        if primera_linea.startswith("type "):
            tipo_obj = primera_linea.split(" ")[1]
        elif primera_linea.startswith("tree "):
            tipo_obj = "commit"
        else:
            tipo_obj = "blob"
    
        # 3. Devolvemos el tipo detectado y la DATA ORIGINAL intacta del archivo
        return tipo_obj, data