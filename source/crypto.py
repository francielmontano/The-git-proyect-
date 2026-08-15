import hashlib
from pathlib import Path


def obtener_hash(ruta_archivo):
    sha1 = hashlib.sha1()
    try:
        with open(ruta_archivo, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()
    except FileNotFoundError:
        return None

def hash_tree(path_or_string_list):

    componentes = []
    for elemento in path_or_string_list:

        if isinstance(elemento, str):
            linea = elemento if elemento.endswith("\n") else f"{elemento}\n"
            componentes.append(linea)

        elif isinstance(elemento, Path):
            hash_actual = obtener_hash(elemento)
            nombre_archivo = elemento.name

            if hash_actual:
                
                linea = f"blob {hash_actual} {nombre_archivo}\n"
                componentes.append(linea)

    componentes.sort()
    string_plano = "".join(componentes)
    data_en_bytes = string_plano.encode("utf-8")

    motor = hashlib.sha1()
    motor.update(data_en_bytes)

    return motor.hexdigest()


def recursive_hash(ruta: Path):

    level = []

    if not ruta.exists() or not ruta.is_dir():
        return None

    ordered_elements = sorted(ruta.iterdir(), key=lambda x: x.name.lower())

    for element in ordered_elements:
        if element.is_dir():
            sub_hash = recursive_hash(element)
            if sub_hash:
                level.append(
                    f"tree {sub_hash} {element.name}\n"
                )

        elif element.is_file():  

            level.append(element)

    if not level:
        return None

    return hash_tree(level)

if __name__ == "__main__":

    ruta = Path(".minigit/commits/commit_2")

    print(recursive_hash(ruta))