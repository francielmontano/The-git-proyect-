from pathlib import Path
from storage.fs import leer_byte, escribir_bytes
def restaurar_imagen():
    archivo_entrada = Path("/home/justin/Documents/The-git-proyect-/.minigit/objects/6f/0fcf6767ef067ec3f9d0ebfe2c3225950634f7")
    archivo_salida = Path("resultado.png")

    if not archivo_entrada.is_file():
        print(f"[Error] No se encuentra el archivo '{archivo_entrada}' en la ruta actual.")
        return

    try:
        contenido_binario = leer_byte(archivo_entrada)

        escribir_bytes(archivo_salida,contenido_binario)

        print(f"[Éxito] ¡Imagen restaurada correctamente como '{archivo_salida}'!")

    except Exception as e:
        print(f"[Error durante el proceso]: {e}")

if __name__ == "__main__":
    restaurar_imagen()