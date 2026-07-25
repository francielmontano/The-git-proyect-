import hashlib

def calculate_file_hash(file_path):
    """
    Lee un archivo en modo binario y genera su hash SHA-1.
    Se usa un buffer (bloques) para no saturar la memoria con archivos grandes.
    """
    sha1 = hashlib.sha1()
    
    try:
        with open(file_path, 'rb') as f:
            # Leemos el archivo en bloques de 64KB
            while chunk := f.read(65536):
                sha1.update(chunk)
        return sha1.hexdigest()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error al calcular el hash: {e}")
        return None

def calculate_string_hash(text):
    """
    Genera un hash SHA-1 de una cadena de texto (útil para metadatos de commits).
    """
    return hashlib.sha1(text.encode('utf-8')).hexdigest()

def verify_integrity(file_path, expected_hash):
    """
    Compara el hash actual de un archivo con un hash esperado.
    Retorna True si son iguales, False si el archivo cambió.
    """
    current_hash = calculate_file_hash(file_path)
    return current_hash == expected_hash