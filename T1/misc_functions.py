from os import path

"""
Aqui van a ir algunas funciones usadas en main.py
"""


def archivo_a_lista() -> list:
    """
    Retorna una lista de listas del archivo "tableros.txt"
    """
    with open(path.join("tableros.txt")) as archivo:
        lineas = archivo.readlines()

    lista = []
    for linea in lineas:
        data = linea.strip().split(",")
        lista.append(data)

    return lista


def existe_tablero(tablero_name: str, tableros: list) -> list:
    """
    Itera por la lista de listas, si el tablero existe, devuelve True
    """
    for data in tableros:
        name = data[0]

        if name == tablero_name:
            return True

    # si paso el loop es porque no esta en la base de datos
    return False


def get_id_tablero(tablero_name: str, tableros: list) -> int:
    """
    Retorna el id en la base de datos del tablero ingresado por el usuario
    """
    for tablero_id in range(len(tableros)):
        name = tableros[tablero_id][0]

        if name == tablero_name:
            return tablero_id

    # si paso el loop es porque no esta en la base de datos
    return -1


def ingresar_datos(name: str, tablero_name: str, tableros: list) -> bool:
    """
    Se asegura que los argumentos dados sean validos
    """
    name_valido = len(name) >= 4 and name.isalpha()
    tablero_valido = existe_tablero(tablero_name, tableros)

    if name_valido and tablero_valido:
        return True

    if not name_valido:
        print("Ese nombre es inválido")

    if not tablero_valido:
        print("Ese tablero no existe")

    return False


def crear_tablero(tablero_list: list) -> list:
    """
    Se recibe a un string de un tablero con sus dimensiones y retorna al tablero como
    lista de listas
    """

    n_filas = int(tablero_list[1])
    n_columnas = int(tablero_list[2])

    body = tablero_list[3:]  # contenido del tablero

    tablero = []

    counter = 0
    for _ in range(n_filas):
        fila = []

        for _ in range(n_columnas):
            fila.append(body[counter])
            counter += 1

        tablero.append(fila)

    return tablero
