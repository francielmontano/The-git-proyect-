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

def generar_hash_tree(lista_de_archivos): 
    componentes = []
    for nombre, hash_archivo in lista_de_archivos:
        linea = f"blob {hash_archivo} {nombre}\n"
        componentes.append(linea)

    componentes.sort()

    string_plano = "".join(componentes)
    data_en_bytes = string_plano.encode('utf-8')

    motor = hashlib.sha1()
    motor.update(data_en_bytes) 

    return motor.hexdigest()

