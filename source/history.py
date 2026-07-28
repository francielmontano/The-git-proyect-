from pathlib import Path
import shutil
from datetime import datetime, date

def create_commit() -> tuple:
    """La función crea automáticamente un nuevo directorio de commit con un nombre secuencial"""
    
    ruta = Path(".minigit/commits")
    _prefijo='commit'
    existentes = [d.name for d in ruta.iterdir() if d.is_dir() and d.name.startswith(_prefijo)]

    num_next = len(existentes) + 1

    new_dir = ruta / f'{_prefijo}_{num_next}'
    new_dir.mkdir()
    sub_dir = new_dir / "metadata"
    sub_dir.mkdir()
        
    return new_dir,sub_dir

def move_stagin(ruta: Path) -> str | None:
    """Copia los archivos que estan en el staging a la carpeta del commit correspondiente"""
    
    staging = Path('.minigit/index')
    ruta.mkdir(parents=True, exist_ok=True)
    if not any(staging.iterdir()):
            return "No existen archivos en la etapa de stagin. Agrege sus archivos"
    for archivo in staging.iterdir():
        
        if archivo.is_dir():
            shutil.copytree(archivo,ruta/archivo.name,dirs_exist_ok=True)
        else:
            shutil.copy2(archivo,ruta)

def meta_data(comentario: str, hash: str, ruta ,pre_hash: str = None):
    """Crea un archivo txt con la metadata del commit """
    
    usuario = Path.home().name
    fecha_actual = datetime.now().astimezone()
    fecha_formateada = f"{int(fecha_actual.timestamp())} {fecha_actual.strftime('%z')}"
    texto = f"""tree {hash}
parent {pre_hash}
author {usuario}
date {fecha_formateada}
----------------------------------
{comentario}
----------------------------------
"""
    
    with open(ruta / "metadata.txt", "w", encoding ="utf-8") as f:
        f.write(texto)
