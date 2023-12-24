"""
Funciones utilizadas para iterar por el laberinto
"""


def find_pos(laberinto: list[list], casilla: str) -> tuple:
    """
    Busca y retorna la primera instancia de la casilla indicada en el argumento, si no existe esa
    casilla, retorna una tupla vacia
    """
    for id_fila in range(len(laberinto)):
        for id_columna in range(len(laberinto[0])):
            celda = laberinto[id_fila][id_columna]
            if celda == casilla:
                return (id_fila, id_columna)

    return ()


def get_columna(laberinto: list[list], columna: int) -> list:
    """
    Dado un laberinto y el numero de una columna. Retorna una lista unidimensional que representa a
    la columna.
    """
    lista = []

    # llegamos a la columna deseada
    for id_fila in range(len(laberinto)):
        for id_columna in range(len(laberinto[0])):
            # si la celda es parte de esa columna, la añadimos a la lista
            if id_columna == columna:
                celda = laberinto[id_fila][id_columna]
                lista.append(celda)

    return lista


def in_between(num: int, n1: int, n2: int) -> bool:
    """
    Retorna True si es que num esta entre n1 y n2, independiente del orden entre estos
    """
    if (n1 < num < n2) or (n2 < num < n1):
        return True
    return False


# TODO: modularizar comportamiento para reducir funcio
def riesgo_lobo(laberinto: list[list],
                posicion_conejo: tuple,
                posicion_lobo: tuple) -> bool:
    pass
