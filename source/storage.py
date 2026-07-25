import shutil
from pathlib import Path

_main_dir = Path('.minigit')

def make_dir() -> str:

    if _main_dir.exists():
        return "El repositorio local ya ha sido inicializado"
        
    (_main_dir / "index").mkdir(parents=True,exist_ok=True)
    (_main_dir / "commits").mkdir(parents=True,exist_ok=True)

    return "El repositorio ha sido inicializado con exito!"


def copy_staging(file: str) -> None:

    if not Path('.minigit').exists():
        return "Error: No existe un repositorio iniciado: .minigit"

    path_origin = Path(file)
    complete_dir = _main_dir / "index" / path_origin.name
    
    if path_origin.exists():
        if path_origin.is_file():
            shutil.copy2(path_origin,complete_dir)

        elif path_origin.is_dir():
            shutil.copytree(path_origin, complete_dir , dirs_exist_ok=True)

        else:
            return f"Error: El archivo o carpeta '{file}' no existe."

    return None