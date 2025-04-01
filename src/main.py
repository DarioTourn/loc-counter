"""
Descripción: Interface de línea de comandos para el contador de líneas de código.
Permite al usuario especificar el directorio a analizar y el tipo de archivo.
Autor: Darío Tourn
Fecha: 01/04/2025
Versión: 1.0
"""
from src.loc_counter import count_loc_in_file


def _analizar_archivo(file_path):
    """Función que analiza un archivo y cuenta las líneas de código.
    Args:
        file_path (str): Ruta del archivo a analizar.
    """
    return count_loc_in_file(file_path)


def analizar_directorio(directory_path):
    """Función que analiza un directorio en busca de archivos .py y cuenta las líneas de código.
    Args:
        directory_path (str): Ruta del directorio a analizar.
    """
    # TODO: Recorrer el directoio en busca de archivos .py y contar las líneas de código.


def main():
    """Función principal que se ejecuta al iniciar el script.
    Permite al usuario especificar un directorio o archivo a analizar.
    """
    # TODO: Crear un parser de argumentos para recibir el directorio o archivo a analizar.


if __name__ == "__main__":
    main()
