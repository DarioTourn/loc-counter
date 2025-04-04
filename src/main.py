"""
Descripción: Interface de línea de comandos para el contador de líneas de código.
Permite al usuario especificar el directorio a analizar y el tipo de archivo.
Autor: Darío Tourn
Fecha: 01/04/2025
Versión: 1.0
"""
import argparse
import os

from loc_counter import count_loc_in_file


def _analizar_archivo(file_path:str) -> dict:
    """Función que analiza un archivo y cuenta las líneas de código.
    Args:
        file_path (str): Ruta del archivo a analizar.
    Returns:
        dict: Diccionario con el conteo de líneas de código; incluyendo tamaño total del archivo,
        cantidad y nombre de clases, cantidad de metodos de cada una de ellas y cantidad
        de funciones.
    """
    return count_loc_in_file(file_path)


def _analizar_directorio(directory_path:str) -> list[str]:
    """Función que analiza un directorio en busca de archivos .py.
    Args:
        directory_path (str): Ruta del directorio a analizar.
    Returns:
        list[str]: file_paths de los archivos .py encontrados en el directorio.
    """
    result = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                result.append(file_path)

    return result


def main():
    """Función principal que se ejecuta al iniciar el script.
    Permite al usuario especificar un directorio o archivo a analizar.
    """

    paths_need_validation = True

    parser = argparse.ArgumentParser(description="Contador de líneas lógicas de código en Python.")
    grupo_exc = parser.add_mutually_exclusive_group(required=True)
    grupo_exc.add_argument("-d", "--directory", help="Ruta del directorio a analizar.")
    grupo_exc.add_argument("-f", "--file", nargs="+", help="Ruta del/los archivo/s a analizar.")

    args = parser.parse_args()
    dir_path, files_paths = vars(args).values()

    # Si el usuario especifica un directorio, lo analizo y obtengo los paths de los archivos .py.
    if dir_path:
        if not os.path.isdir(dir_path):
            print(f'El directorio "{dir_path}" no existe.')
            return

        files_paths = _analizar_directorio(dir_path)
        # Los paths provienen de la recorrida del directorio. No necesito validar que existan.
        paths_need_validation = False

    for file in files_paths:
        if paths_need_validation:
            if not os.path.isfile(file):
                print(f'El archivo "{file}"" no existe.')
                continue
            if not file.endswith(".py"):
                print(f'El archivo "{file}" no es un archivo Python.')
                continue

        # Si el archivo existe y es un archivo Python, lo analizo e imprimo el resultado.
        result = _analizar_archivo(file)
        print(f"Archivo: {result['file_name']}")
        print(f"Total de líneas lógicas: {result['total_lines']}")

        if "classes" in result:
            print("Clases:")

            for _, class_data in result["classes"].items():
                print(f"\tClase: {class_data['class_name']}")
                print(f"\tCantidad de líneas: {class_data['total_lines']}")

                if "methods" in class_data:
                    print("\tMétodos:")
                    for _, method_data in class_data["methods"].items():
                        print(f"\t\tNombre: {method_data['method_name']}")
                        print(f"\t\tCantidad de líneas: {method_data['total_lines']}\n")
                else:
                    print("\tNo se encontraron métodos en esta clase.\n")
        else:
            print("No se encontraron clases en este archivo.")
        print("\n")


if __name__ == "__main__":
    main()
