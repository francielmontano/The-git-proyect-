from pathlib import Path
import tempfile
def crear_directorio(ruta: Path):
    """Crea el directorio si no existe."""
    Path(ruta).mkdir(parents=True, exist_ok=True)

def exists(path: str) -> bool:
    """Verifica si un archivo o directorio existe."""
    return Path(path).exists()

def leer_byte(ruta: str):
    verificar = exists(ruta)
    if verificar:
        bytes_content: bytes = Path(ruta).read_bytes()
        return bytes_content
    return None

def escribir_bytes(ruta: str, datos: bytes):
    target = Path(ruta)
    verificar = exists(ruta)
    if verificar:
        target.write_bytes(datos)