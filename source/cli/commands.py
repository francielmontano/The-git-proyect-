import socket
from pathlib import Path
from typing import Annotated
import typer
from rich import print
from core.repository import Repository

# Instanciamos ÚNICAMENTE la clase principal
repo = Repository()

app = typer.Typer(
    name="minigit",
    help="Mi propia herramienta de control de versiones tipo Git",
    add_completion=False
)

@app.command()
def init():
    """Inicia un nuevo repositorio"""
    repo.init()

@app.command()
def add(
    target: str = typer.Argument(
        ...,
        help="Nombre del archivo o '.' para todos los archivos."
    ),
    remove: bool = typer.Option(
        False,
        "-r",
        "--rm",
        "--remove",
        help="Elimina el archivo especificado del área de preparación (staging)."
    )
):
    """Agrega o elimina archivos del área de preparación."""
    
    # === MODO ELIMINAR/REMOVER (-r / --remove) ===
    if remove:
        if target == ".":
            # Vacía todo el index.json usando el método de Repository
            repo.clear_index()
            print("[bold yellow]Se ha vaciado todo el index.json.[/bold yellow]")
            return

        # Si se especificó un archivo particular
        path = Path(target)
        clean_path = str(path.as_posix())
        repo.remove(clean_path)
        print(f"[yellow]Removido del index:[/yellow] {clean_path}")
        return

    # === MODO AGREGAR (target == ".") ===
    if target == ".":
        archivos_encontrados = []
        for path in Path(".").rglob("*"):
            if path.is_file() and not any(p.startswith(".minigit") for p in path.parts):
                archivos_encontrados.append(str(path.as_posix()))
        
        for clean_path in archivos_encontrados:
            resultado = repo.add(clean_path)
            if resultado == "Error: No existe un repositorio iniciado: minigit init":
                print(f"[bold red]{resultado}[/bold red]")
                raise typer.Exit(code=1)
        return

    # === MODO AGREGAR ARCHIVO ÚNICO ===
    path = Path(target)
    if not path.exists():
        print(f"[bold red]Error:[/bold red] El archivo '{target}' no existe.")
        raise typer.Exit(code=1)

    clean_path = str(path.as_posix())
    resultado = repo.add(clean_path)

    if resultado == "Error: No existe un repositorio iniciado: minigit init":
        print(f"[bold red]{resultado}[/bold red]")
        raise typer.Exit(code=1)

@app.command()
def commit(
    message: Annotated[str, typer.Option(..., '-m', "--message", help="Mensaje del commit")]
):
    author = socket.gethostname()
    repo.commit(author, message)

@app.command()
def log():
    repo.log()