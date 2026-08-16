from pathlib import Path

def crear_directorio(ruta: Path):
    """Crea el directorio si no existe."""
    Path(ruta).mkdir(parents=True, exist_ok=True)

def exists(path: Path) -> bool:
    """Verifica si un archivo o directorio existe."""
    return Path(path).exists()

def leer_byte(ruta: Path):
    verificar = exists(ruta)
    if verificar:
        bytes_content: bytes = Path(ruta).read_bytes()
        return bytes_content
    return None

def escribir_bytes(ruta:Path, datos):
    Path(ruta).write_bytes(datos)
    