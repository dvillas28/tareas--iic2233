from utils.utils_cliente import find_pos, get_columna, in_between


def validacion_formato(nombre: str) -> bool:
    """
    Un nombre es valido si: Es alfanumerico, tiene al menos una Mayus, y al menos un numero.
    Ademas 3 <= largo <= 16
    """
    alfanumerico: bool = nombre.isalnum()
    al_menos_una_mayus: bool = False
    al_menos_un_numero: bool = False

    for letra in nombre:
        if letra.isupper():
            al_menos_una_mayus = True

        elif letra.isdigit():
            al_menos_un_numero = True

    if alfanumerico and al_menos_una_mayus and al_menos_un_numero:
        if 3 <= len(nombre) <= 16:
            return True

    return False


def riesgo_mortal(laberinto: list[list]) -> bool:
    """
    Retorna True si el conejo puede morir estando en esa posicion, debido a una posible colision
    con algun lobo o una zanahoria salida de un cañon
    """
    # primero buscamos al conejo
    pos_conejo = find_pos(laberinto, "C")

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
                                        return False
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
                                        return False
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
                                        return False
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
                                        return False
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
                                        return False
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
                                        return False
                            return True

    # si se recorrio todo el tablero, es porque no se hallo riesgo
    return False


def usar_item(item: str, inventario: list) -> tuple[bool, list]:
    """
    Si el item esta en el inventario, retorna una tupla con True y el inventario con el item
    removido, si no lo esta, retorna una tupla con False y el inventario sin modificar
    """

    if item not in inventario:
        return (False, inventario)

    inventario.remove(item)
    return (True, inventario)


def calcular_puntaje(tiempo: int, vidas: int, cantidad_lobos: int, PUNTAJE_LOBO: int) -> float:
    try:
        valor = round((tiempo * vidas) / (cantidad_lobos * PUNTAJE_LOBO), 2)

    except ZeroDivisionError:
        valor = 0.0

    return valor


def validar_direccion(laberinto: list[list], tecla: str) -> bool:
    pos_conejo = find_pos(laberinto, "C")
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
