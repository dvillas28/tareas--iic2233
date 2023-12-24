def riesgo_mortal(laberinto: list[list], pos_conejo: list) -> bool:
    """
    Retorna True si el conejo puede morir estando en esa posicion, debido a una posible colision
    con algun lobo o una zanahoria salida de un cañon
    """
    # primero buscamos al conejo
    # pos_conejo = find_pos(laberinto, "C")
    for id_fila in range(len(laberinto)):
        for id_columna in range(len(laberinto[0])):
            celda = laberinto[id_fila][id_columna]
            if (len(celda) == 2):
                # es un lobo
                if celda[0] == "L":

                    if celda[1] == "V":
                        # es vertical, revisamos que esten en la misma columna
                        if id_columna == pos_conejo[1]:
                            # a la primera celda que este entre medio de los dos, ya no hay riesgo
                            columna: list = get_columna(laberinto, id_columna)
                            for value in range(len(columna)):
                                if "P" == columna[value]:
                                    # si hay P en medio, no hay riesgo
                                    if in_between(value, id_fila, pos_conejo[0]):
                                        # print('safe_verti')
                                        # return False
                                        break
                            # no hay ningun P entre medio, hay riesgo de morir
                            return True

                    elif celda[1] == "H":
                        # es horizontal, revisamos que enten en la misma fila
                        if id_fila == pos_conejo[0]:
                            fila: list = laberinto[id_fila]
                            for value in range(len(fila)):
                                if "P" == fila[value]:
                                    # si hay P en medio, no hay riesgo
                                    if in_between(value, id_columna, pos_conejo[1]):
                                        # print('safe_hori')
                                        break
                            # no hay ningun P entre medio, hay riesgo de morir
                            return True

                # es un cañon
                elif celda[0] == "C":

                    # arriba
                    if celda[1] == "U":
                        # si esta en la misma columna y sobre el cañon
                        if (id_columna == pos_conejo[1]) and (pos_conejo[0] < id_fila):
                            columna: list = get_columna(laberinto, id_columna)
                            # iterar hasta la posicion del cañon
                            for value in range(id_fila):
                                if "P" == columna[value]:
                                    if in_between(value, id_fila, pos_conejo[0]):
                                        break
                            return True

                    # abajo
                    elif celda[1] == "D":
                        # si esta en la misma columna y por debajo del cañon
                        if (id_columna == pos_conejo[1]) and (pos_conejo[0] > id_fila):
                            columna: list = get_columna(laberinto, id_columna)
                            # iterar desde la posicion del canon
                            for value in range(id_fila, len(columna)):
                                if "P" == columna[value]:
                                    if in_between(value, id_fila, pos_conejo[0]):
                                        break
                            return True

                    # izquierda
                    elif celda[1] == "L":
                        # si esta en la misma fila y a la izquierda del cañon
                        if (id_fila == pos_conejo[0]) and (pos_conejo[1] < id_columna):
                            fila: list = laberinto[id_fila]
                            # iterar hasta la posicion del cañon
                            for value in range(id_columna):
                                if "P" == fila[value]:
                                    if in_between(value, id_columna, pos_conejo[1]):
                                        break
                            return True

                    # derecha
                    elif celda[1] == "R":
                        # si esya en la misma fila y a la derecha del cañon
                        if (id_fila == pos_conejo[0]) and (pos_conejo[1] > id_columna):
                            fila: list = laberinto[id_fila]
                            # iterar desde la posicion del cañon
                            for value in range(id_columna, len(fila)):
                                if "P" == fila[value]:
                                    if in_between(value, id_columna, pos_conejo[1]):
                                        break
                            return True

    # si se recorrio todo el tablero, es porque no se hallo riesgo
    return False


def validar_direccion(laberinto: list[list], pos_conejo: list, tecla: str) -> bool:
    """
    Cambio respecto a la entrega intermedia: añadi la posicion del conejo como parametro
    Ya que necesito ir cambiando de posicion continuamente
    """

    # pos_conejo = find_pos(laberinto, "C")
    casillas_solidas = ("P", "CU", "CD", "CL", "CR")

    if tecla == "W":  # arriba
        if pos_conejo[0] - 1 >= 0:  # no salirse por arriba
            if laberinto[pos_conejo[0] - 1][pos_conejo[1]] not in casillas_solidas:
                return True

    elif tecla == "S":  # atras
        if pos_conejo[0] + 1 <= len(laberinto):  # no salirse por abajo
            if laberinto[pos_conejo[0] + 1][pos_conejo[1]] not in casillas_solidas:
                return True

    elif tecla == "A":  # izquierda
        if pos_conejo[1] - 1 >= 0:  # no salirse por la izq
            if laberinto[pos_conejo[0]][pos_conejo[1] - 1] not in casillas_solidas:
                return True

    elif tecla == "D":  # derecha
        if pos_conejo[1] + 1 <= len(laberinto[0]):  # no salirse por la der
            if laberinto[pos_conejo[0]][pos_conejo[1] + 1] not in casillas_solidas:
                return True
    return False


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


def generador_secuencia():
    """
    1, 2, 3, 1, 2, 3. Necesaria para ir iterando por los pixmaps
    """

    x = 1

    while True:

        if x == 1:
            yield 1
            x = 2

        elif x == 2:
            yield 2
            x = 3

        elif x == 3:
            yield 3
            x = 1
