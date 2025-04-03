"""
Descripción: Contador de líneas de código en Python.
Autor: Darío Tourn
Fecha: 01/04/2025
Versión: 1.0
"""
def count_loc_in_file(file_path:str) -> dict:
    """Función que analiza un archivo y cuenta las líneas de código.
    Args:
        file_path (str): Ruta del archivo a analizar.
    Returns:
        dict: Diccionario con el conteo de líneas de código; incluyendo tamaño total del archivo,
        cantidad y nombre de clases, cantidad de metodos de cada una de ellas y cantidad
        de funciones.
    """
