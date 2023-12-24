from tablero_functions import (get_peones_invalidos,
                               get_piezas_explosivas)
from copy import (copy,
                  deepcopy)


def get_celdas_vacias(tablero) -> list:
    """
    Dado el tablero, obtiene las celdas (vacias) que de ellas depende que se
    resuelva el tablero. Es decir recorremos la lista del tablero y vamos
    descartando:
    - posiciones de bombas
    - posiciones de PP ya colocados
    """

    lista_criticas = []

    for id_fila in range(tablero.dimensiones[0]):
        for id_columna in range(tablero.dimensiones[1]):
            celda = tablero.tablero[id_fila][id_columna]
            # si la celda es una bomba
            if celda[0] in "VHR":
                continue
            # si la celda es un PP
            if celda == "PP":
                continue
            # si la celda esta vacia, debemos checkear que afecte en algo
            if celda == "--":
                lista_criticas.append([[id_fila, id_columna], 0])

    return lista_criticas


def solver_recursivo(tablero, index: int, lista_criticas: list) -> list:
    """
    Funcion que recibe una lista de posiciones criticas (celdas vacias) y va probando todas las
    combinaciones posibles entre poner un PP o dejar una celda vacia, luego esta combinacion se
    valida si es solucion y se devuelve una lista de listas con las soluciones. En caso de que no
    haya solucion, se retorna una lista vacia
    """
    # lista criticas -> [[[posicion], PP/--], ...]

    # se llego al final
    if index == len(lista_criticas):
        # aplicamos cambios y comprobamos si es solucion
        if condicion_solucion(tablero, lista_criticas):
            sol = deepcopy(tablero.tablero)
            return [sol]  # si lo es añadimos la sol a una lista
        return []

    # primer elemento a PP
    lista_criticas[index][1] = "PP"
    combinaciones_pp = solver_recursivo(
        tablero, index + 1, copy(lista_criticas))

    # primer elemento a --
    lista_criticas[index][1] = "--"
    combinaciones_vacia = solver_recursivo(
        tablero, index + 1, copy(lista_criticas))

    # retornamos todas las combinaciones que lograron pasar la condicion de solucion
    return combinaciones_pp + combinaciones_vacia


def aplicar_cambios(tablero: list, lista_de_cambios: list) -> list:
    """
    Recibe una lista de listas donde cada lista es una que contiene la posicion donde debe
    colocarse o un PP o un --. Iterando sobre la lista se va aplicando posicion por posicion en el
    tablero, el tipo de celda que indica lista_de_cambios
    """

    for cambio in lista_de_cambios:
        coords = cambio[0]  # coordenadas del cambio, lista
        a_cambiar = cambio[1]  # tipo de celda a cambiar (PP/--)

        tablero[coords[0]][coords[1]] = a_cambiar
    return tablero


def condicion_solucion(tablero, lista_de_cambios: list) -> bool:
    """
    Funcion que llama a aplicar los cambios a un tablero y luego llama  a otra funcion
    que comprueba si es que esa configuracion de piezas es solucion
    """

    nuevo_tablero = aplicar_cambios(tablero.tablero, lista_de_cambios)
    tablero.tablero = copy(nuevo_tablero)
    if esta_el_tablero_resuelto(tablero):
        return True
    return False


def esta_el_tablero_resuelto(tablero) -> bool:
    """
    En un tablero resuelto, cada ficha explosiva cumple que su alcance es igual al numero reportado
    y cada pieza PP tiene a lo mas 1 vecino PP
    """
    # check regla1:
    lista_piezas_explosivas = get_piezas_explosivas(tablero)

    # check regla3
    peones_invalidos = get_peones_invalidos(tablero)

    if peones_invalidos != 0:
        return False

    for pieza_explosiva_pos in lista_piezas_explosivas:
        id_fila = pieza_explosiva_pos[0]
        id_columna = pieza_explosiva_pos[1]

        pieza_str = tablero.tablero[id_fila][id_columna]
        celdas_a_destruir = int(pieza_str[1:])

        alcance_total = tablero.celdas_afectadas(id_fila, id_columna)

        # si hay una sola que no cumpla es porque el tablero no esta resuelto
        if celdas_a_destruir != alcance_total:
            return False

    return True
