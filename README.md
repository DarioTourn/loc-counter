Programa contador de líneas lógicas de código, siguiendo los estándares especificados a continuación:
| **Tipo de Conteo**  | **Tipo**   | **Comentarios** |
|---------------------|-----------|----------------|
| **Físico/Lógico**  | Lógico    |                |

| **Tipo de Sentencia**  | **Incluida** | **Comentarios** |
|-----------------------|------------|----------------|
| **Ejecutable**       | Sí         | Llamadas a funciones, returns |
| **No ejecutable**    |            |                |
| **Declaraciones**    | Sí         | Incluye declaraciones de funciones, variables y clases. Las declaraciones multilínea (ejemplo: una lista) se cuentan solo una vez. |
| **Directivas del Intérprete** | Sí | Imports |
| **Comentarios**      | No        | Comentarios de una línea y doc-strings no se cuentan. |
| **Líneas en blanco** | No        |                |

| **Aclaraciones**| | **Ejemplos/Casos** |
|-----------------|-|----------------|
| **Sentencias vacías** | No ||
| **Instanciaciones genéricas** | No ||
| **Palabras clave** | Sí | Contar una línea por cada ocurrencia de las siguientes palabras clave: `switch`, `case`, `break`, `continue`, `if`, `else`, `elif`, `for`, `while`, `try`, `except`, `finally`, `raise`, `with`, `lambda`, etc. |
