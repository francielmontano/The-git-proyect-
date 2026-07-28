from pathlib import Path
import shutil
from datetime import datetime, timezone, timedelta
from crypto import obtener_hash

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
        shutil.move(archivo, ruta / archivo.name)



def meta_data(comentario: str, hash: str, ruta: Path ,pre_hash: str = ""):
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



def command_log() -> None:
    """Imprime en pantalla el contenidos de los metadatos de todos los commits"""

    main_dir = Path(".minigit/commits")

    ordered_files = sorted(
        main_dir.iterdir(), 
        key=lambda x: int(x.stem.split('_')[-1]) if '_' in x.stem else 0
    )

    for file in ordered_files:
        metadata = file / "metadata/metadata.txt"

        lines = metadata.read_text(encoding='utf-8').splitlines()

        unix_str, offset_str = lines[3].split()[1], lines[3].split()[2]

        commit_hash = obtener_hash(metadata)
        date = datetime.fromtimestamp(int(unix_str), timezone(timedelta(hours=int(offset_str[:3]))))
        final_date = date.strftime("%a %b %d %H:%M:%S %Y %z")
        autor = lines[2].split()[1]
        coment = lines[5]

        log = f"""
        commit {commit_hash}
        Autor: {autor}
        date: {final_date}

            {coment}
        """
        print(log)
        
    return None