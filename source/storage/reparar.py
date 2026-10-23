from pathlib import Path
from storage.fs import leer_byte, escribir_bytes
def restaurar(archivo_entrada, archivo_salida):
    ruta_entrada = Path(archivo_entrada)
    ruta_salida = Path(archivo_salida)
    if not archivo_entrada.is_file():
        print(f"[Error] No se encuentra el archivo '{ruta_entrada}' en la ruta actual.")
        return

    try:
        contenido_binario = leer_byte(ruta_entrada)

        escribir_bytes(ruta_salida,contenido_binario)

        print(f"[Éxito] archivo restaurado correctamente '{ruta_salida}'!")

    except Exception as e:
        print(f"[Error durante el proceso]: {e}")
