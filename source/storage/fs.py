from pathlib import Path
import tempfile
def crear_directorio(ruta_str: str, es_archivo: bool = False):
    ruta = Path(ruta_str)
    if es_archivo:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.touch(exist_ok=True)
    else:
        ruta.mkdir(parents=True, exist_ok=True)

def exists(path: str) -> bool:
    """Verifica si un archivo o directorio existe."""
    return Path(path).exists()

def leer_byte(ruta):
    objeto_ruta = Path(ruta)
    if objeto_ruta.is_file():
        return objeto_ruta.read_bytes()
    else: return None

def escribir_bytes(ruta: str, datos: bytes):
    target = Path(ruta)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(datos)

def listar_contenido(ruta_carpeta: str):
    carpeta = Path(ruta_carpeta)
    if carpeta.is_dir():
        return [elemento for elemento in carpeta.iterdir()]
    return None