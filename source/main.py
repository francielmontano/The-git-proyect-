from typing import Annotated
import typer 
import storage
import history
import crypto
from pathlib import Path
import shutil

app = typer.Typer(
    name = "minigit",
    help = "Mi propia herramienta de control de versiones tipo Git",
    add_completion = False
)

def pre_hash() -> None | str:
    """Coloca el hash del commit anterior al nuevo como parent"""
    
    ruta = Path(".minigit/commits")
    lista = sorted(ruta.iterdir())
    
    if not ruta.exists() or not ruta.is_dir():
        return None

    ruta_metadata = lista[-1] / "metadata" / "metadata.txt"

    if not ruta_metadata.exists():
        return None

    with open(ruta_metadata,"r",encoding="utf-8") as f:
        file = f.read().split("\n")[0].split(" ")[1]
    return file

@app.command()
def init():
    """Inicia un nuevo repositorio"""
    print(storage.make_init())

@app.command()
def add(
    archivo =typer.Argument(None)
) -> None:
    """Agrega uno o varios archivos para subirlos a tu commit"""
    if archivo:
        if archivo == ".":
            ruta = Path.cwd()
            for f in ruta.iterdir():
                if f == Path(ruta / ".minigit"):
                    continue
                storage.copy_staging(f)
        elif storage.copy_staging(archivo) != None:
            print(storage.copy_staging(archivo))

@app.command()
def commit(
    message: Annotated[str, typer.Option(...,'-m',"--message", help="Mensaje del commit")]
) -> None:
    """Guarda tu commit junto a sus metadatos"""

    comentario: str = message
    ruta_index = Path(".minigit/index")
    
    if not any(ruta_index.iterdir()):
        print( "No existen archivos en la etapa de staging. Agrege sus archivos con 'minigit add'")
        return None

    hash_pre = pre_hash()
    hash = crypto.hash_tree(list(ruta_index.iterdir()))
    rutas_history = history.create_commit()
    history.move_stagin(rutas_history[0])
    
    history.meta_data(comentario,hash,rutas_history[1],hash_pre)

@app.command()
def log() -> None:
    """Imprime en pantalla el contenidos de los metadatos de todos los commits"""

    history.command_log()

if __name__ == "__main__":
    app()