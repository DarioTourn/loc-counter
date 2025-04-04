"""
Descripción: Contador de líneas de código en Python.
Autor: Darío Tourn
Fecha: 01/04/2025
Versión: 1.0
"""
import re
def count_loc_in_file(file_path:str) -> dict:
    """Función que analiza un archivo y cuenta las líneas de código.
    Args:
        file_path (str): Ruta del archivo a analizar.
    Returns:
        dict: Diccionario con el conteo de líneas de código; incluyendo tamaño total del archivo,
        cantidad y nombre de clases, cantidad de metodos de cada una de ellas y cantidad
        de funciones.
    """
    file_total_lines = 0

    classes = {}
    class_count = 0 # Cantidad de clase detectadas

    # Contexto de la clase actual
    current_class_total_lines = 0 # Cantidad de lineas de la clase actual
    current_class_name = ''
    current_class_indentation_level = 0 # Nivel de indentacion de la clase actual.
                                        # Cada nivel aumenta de a 4 espacios.

    has_methods = False # Indica si la clase tiene metodos
    current_class_methods = {}
    current_class_methods_count = 0 # Cantidad de metodos de la clase actual

    # Contexto del metodo actual
    current_method_name = ''
    current_method_lines = 0 # Cantidad de lineas del metodo actual
    current_method_indentation_level = 0 # Nivel de indentacion de la clase actual.

    # Abro el archivo
    with open(file_path, 'r') as file:

        for line in file:
            # Calculo el nivel de indentacion de la linea actual
            indentation_level = _indentation_level(line)

            # Verifico si es un import
            if bool(re.search(r'^(from\s+\w+\s+import\s+(\w+|\*)|import\s+\w+(\s+as\s+\w+)?)',
                              line, re.VERBOSE)):
                file_total_lines += 1
                continue

            # Verifico si es una declaraccion de clase
            class_match = re.match(r'^\s*class\s+(\w+)', line, re.VERBOSE)
            # FIXME: No se contempla el caso de las clases anidadas.
            if class_match:
                class_count += 1

                # Si ya hay una clase siendo contabilizada, guardo su informacion.
                # Se hace diempre, salvo la primera vez que se encuentra una clase.
                if class_count > 1:
                    # Guardamos la información de la clase anterior en el diccionario
                    # Primero guardo la información del método actual, si existe
                    if has_methods:
                        (current_method_name,
                         current_method_lines,
                         current_method_indentation_level) = _save_method(current_class_methods,
                                                                  current_method_name,
                                                                  current_method_lines,
                                                                  current_method_indentation_level)

                    # Ahora guardo la información de la clase actual
                    (current_class_total_lines,
                     current_class_name,
                     has_methods, current_class_methods_count) = _save_class(classes,
                                                                       current_class_name,
                                                                       current_class_total_lines,
                                                                       has_methods,
                                                                       current_class_methods_count,
                                                                       current_class_methods)

                # Ahora sí, comienzo a contar la nueva clase
                file_total_lines += 1
                current_class_total_lines += 1
                current_class_name = class_match.group(1)
                current_class_indentation_level = indentation_level
                continue

            # Verifico si es una declaracion de un método de clase
            # Primero veo que tenga la estructura de la un metodo
            function_match = re.match(r'^\s*def\s(\w+)', line, re.VERBOSE)
            if function_match:
                # Contemplamos la indentacion para definir si es un metodo de la clase actual o no.
                # Contempla el caso de que no estemos dentro de una clase.
                # Si está indentado un nivel más que la clase actual, es un método de esta clase.
                if indentation_level == current_class_indentation_level + 1:
                    current_class_methods_count += 1
                    has_methods = True

                    # Si ya hay un metodo siendo contabilizado, guardo su informacion.
                    # Se hace siempre, salvo la primera vez que se encuentra un método.
                    if current_class_methods_count > 1:
                        (current_method_name,
                         current_method_lines,
                         current_method_indentation_level) = _save_method(current_class_methods,
                                                                  current_method_name,
                                                                  current_method_lines,
                                                                  current_method_indentation_level)

                    # Ahora sí, comienzo a contar el nuevo método
                    current_method_name = function_match.group(1)
                    current_class_total_lines += 1
                    current_method_lines += 1
                    current_method_indentation_level = indentation_level
                elif  indentation_level > current_class_indentation_level + 1:
                    # Está dentro de un método o de una clase interna,
                    # pero no es un método de la clase actual.
                    current_class_total_lines += 1

                # Finalmente, aún si: indentation_level <= current_class_indentation_level,
                # lo contamos como una linea "general".
                # Estamos fuera de cualquier clase. Puedo estar saliendo o ya estar afuera.
                file_total_lines += 1
                continue

            # Verfico si es una asignacion de variable, un llamado a funcion,
            # una estructura de control u otra palabra reservada
            # (Es decir, una linea de código "general").
            if bool(re.search(r'''
                                ^\s*[\w.-]+\s+(=|\+=|-=|\*=|/=|%=|\*\*=|//=|&=|\|=|\^=|>>=|<<=)\s+.+ # Asignacion de variable
                              | ^\s*\w.+\(.*\) # Llamado a funcion
                              | ^\s*match\s+.+ # Match
                              | ^\s*case\s+.+ # Case
                              | ^\s*if\s+.+ # If
                              | ^\s*elif\s+.+ # Else if
                              | ^\s*else: # Else
                              | ^\s*for\s+.+ # For
                              | ^\s*try\s*: # Try
                              | ^\s*except\s*.*: # Except
                              | ^\s*raise\s+.+ # Raise
                              | ^\s*finally\s*: # Finally
                              | ^\s*with\s+.+: # With
                              | ^\s*while\s+.+ # While
                              | ^\s*return\s*.* # Return
                              | ^\s*break\s*: # Break
                              | ^\s*continue\s*: # Continue
                              | ^\s*assert\s+.+ # Assert
                              | ^\s*del\s+.+ # Del
                              | ^\s*lambda\s+.+ # Lambda
                              | ^\s*async\s+.+ # Async
                              | ^\s*await\s+.+ # Await
                              | ^\s*yield\s+.+ # Yield
                              ''', line, re.VERBOSE)):
                if indentation_level >= current_method_indentation_level + 1:
                    current_method_lines += 1
                    current_class_total_lines += 1

                # Pero menor que el del metodo actual
                elif indentation_level >= current_class_indentation_level + 1:
                    current_class_total_lines += 1

                file_total_lines += 1
                continue

        # Guardamos la información de la clase anterior en el diccionario
        # Primero guardo la información del método actual, si existe
        if class_count >= 1:
            if has_methods:
                (current_method_name,
                current_method_lines,
                current_method_indentation_level) = _save_method(current_class_methods,
                                                        current_method_name,
                                                        current_method_lines,
                                                        current_method_indentation_level)

            # Ahora guardo la información de la clase actual
            (current_class_total_lines,
            current_class_name,
            has_methods, current_class_methods_count) = _save_class(classes,
                                                            current_class_name,
                                                            current_class_total_lines,
                                                            has_methods,
                                                            current_class_methods_count,
                                                            current_class_methods)

        result = {
            'file_name': file_path,
            'total_lines': file_total_lines,
        }
        if class_count > 0:
            result['classes'] = classes
        return result


def _save_class(classes:dict, current_class_name:str,
                 current_class_total_lines:int,
                 has_methods:bool, current_class_method_count,
                 current_class_methods:dict,
                 context_reset=True) -> tuple[int, str, bool, int]:
    """Función que guarda la información de una clase en el diccionario de clases.
    Args:
        classes (dict): Diccionario con las clases.
        class_count (int): Cantidad de clases detectadas.
        current_class_name (str): Nombre de la clase actual.
        current_class_total_lines (int): Cantidad de líneas de la clase actual.
        has_methods (bool): Indica si la clase tiene métodos.
        current_class_methods (dict): Diccionario con los métodos de la clase actual.
    """
    classes[current_class_name] = {
        'class_name': current_class_name,
        'total_lines': current_class_total_lines,
    }
    if has_methods:
        classes[current_class_name]['methods'] = current_class_methods.copy()

    # Reinicio el contexto de la clase actual
    if context_reset:
        current_class_total_lines = 0
        current_class_name = ''
        has_methods = False
        current_class_method_count = 0
        current_class_methods.clear()

    return current_class_total_lines, current_class_name, has_methods, current_class_method_count


def _save_method(current_class_methods:dict, current_method_name:str,
                 current_method_lines:int,
                 current_method_indentation_level:int,
                 context_reset=True) -> tuple[str, int, int]:
    """Función que guarda la info de un método en el diccionario de métodos de la clase actual.
    Args:
        current_class_methods (dict): Diccionario con los métodos de la clase actual.
        current_method_name (str): Nombre del método actual.
        current_method_lines (int): Cantidad de líneas del método actual.
        current_method_indentation_level (int): Nivel de indentación del método actual.
    """
    current_class_methods[current_method_name] = {
        'method_name': current_method_name,
        'total_lines': current_method_lines
    }
    # Reinicio el contexto del método actual
    if context_reset:
        current_method_name = ''
        current_method_lines = 0
        current_method_indentation_level = 0

    return current_method_name, current_method_lines, current_method_indentation_level


def _indentation_level(line:str) -> int:
    """Función que devuelve el nivel de indentación de una línea de código.
    Args:
        line (str): Línea de código.
    Returns:
        int: Nivel de indentación de la línea.
    """
    match = re.match(r"^(\s*)", line)
    return len(match.group(1)) // 4 if match else 0
