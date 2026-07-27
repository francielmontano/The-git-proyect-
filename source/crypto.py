import hashlib

def obtener_hash_archivo(ruta_archivo):
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

def generar_hash_tree(lista_de_archivos): # <--- Corregido nombre y :
    componentes = []
    for nombre, hash_archivo in lista_de_archivos:
        linea = f"blob {hash_archivo} {nombre}\n"
        componentes.append(linea)

    componentes.sort()

    string_plano = "".join(componentes)
    data_en_bytes = string_plano.encode('utf-8')

    motor = hashlib.sha1()
    motor.update(data_en_bytes) # <--- Corregido: agregado la 's'

    return motor.hexdigest()

# ==========================================
# PARA PROBARLO TÚ MISMO:
# ==========================================
if __name__ == "__main__":
    # 1. Obtenemos el hash de un archivo real que tengas (ejemplo: crypto.py)
    h1 = obtener_hash_archivo("source/crypto.py")
    
    # 2. Creamos una lista de prueba usando ese hash
    prueba_lista = [("crypto.py", h1)]
    
    # 3. Llamamos a la segunda función
    id_commit = generar_hash_tree(prueba_lista)
    
    print(f"Hash del archivo: {h1}")
    print(f"Hash del Commit (Tree): {id_commit}")

