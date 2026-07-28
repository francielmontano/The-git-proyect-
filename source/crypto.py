import hashlib
import os

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

def hash_tree(lista_de_rutas):
    componentes = []
    for ruta in lista_de_rutas:
        hash_actual = obtener_hash(ruta)
        nombre_archivo = os.path.basename(ruta)
        
        if hash_actual:
            linea = f"blob {hash_actual} {nombre_archivo}\n"
            componentes.append(linea)

    componentes.sort()
    string_plano = "".join(componentes)
    data_en_bytes = string_plano.encode('utf-8')
    
    motor = hashlib.sha1()
    motor.update(data_en_bytes)
    
    return motor.hexdigest()

if __name__ == "__main__":
    archivos = ["source/crypto.py", "source/storage.py"]
    print(hash_tree(archivos))