from cli.commands import app
import sys
from pathlib import Path
from core.repository import Repository

# Añade el directorio actual ('source') a la ruta de búsqueda de Python
source_dir = Path(__file__).resolve().parent
if str(source_dir) not in sys.path:
    sys.path.insert(0, str(source_dir))

# Ahora tus importaciones funcionarán sin importar de dónde ejecutes el binario
from cli.commands import app

ejemplo = Repository()
ejemplo.restorage("5ba3e34e8237ef6a668f35906efc67421c7e6f52")
if __name__ == "__main__":
    app()   