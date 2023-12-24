
def get_peones_invalidos(tablero) -> int:
    """
    Recibe una instancia de Tablero y retorna el numero de peones invalidos en este. Se toman los
    peones y sus posciones, luego por cada uno de los peones se revisa cuantos vecinos tiene
    """
    peones = []  # [pos1, pos2, pos3....]

    # iterar sobre el tablero
    for id_fila in range(tablero.dimensiones[0]):
        for id_columna in range(tablero.dimensiones[1]):
            celda = tablero.tablero[id_fila][id_columna]

            if celda == "PP":

                # obtener una lista de listas con las posiciones de todos los peones
                peones.append([id_fila, id_columna])

    peones_invalidos = 0
    for peon_pos in peones:
        numero_vecinos = 0

        # revisar vecino arriba (fila - 1, col)
        # limite_sup. de filas
        if (peon_pos[0] - 1) >= 0:
            celda = tablero.tablero[peon_pos[0] - 1][peon_pos[1]]
            if celda == "PP":
                numero_vecinos += 1

        # revisar vecino abajo (fila + 1, col)
        # limite inf. de filas
        if (tablero.dimensiones[0] - 1) >= (peon_pos[0] + 1):
            celda = tablero.tablero[peon_pos[0] + 1][peon_pos[1]]
            if celda == "PP":
                numero_vecinos += 1

        # revisar vecino derecha (fila, col + 1)
        # limite der. de columnas
        if (tablero.dimensiones[1] - 1) >= (peon_pos[1] + 1):
            celda = tablero.tablero[peon_pos[0]][peon_pos[1] + 1]
            if celda == "PP":
                numero_vecinos += 1

        # revidar vecino izquierda (fila, col - 1)
        # limite izq. de columnas
        if (peon_pos[1] - 1) >= 0:
            celda = tablero.tablero[peon_pos[0]][peon_pos[1] - 1]
            if celda == "PP":
                numero_vecinos += 1

        # si la cantidad de vecinos es > 1, es un vecino invalido
        if numero_vecinos > 1:
            # vecino invalido
            peones_invalidos += 1

    # retornar el n de peones tablero
    return peones_invalidos


def get_columna(tablero, columna: int) -> list:
    """
    Dado un Tablero y el numero de una columna. Retorna una lista unidimensional que representa a
    la columna.
    """
    lista = []

    # llegamos a la columna deseada
    for id_fila in range(tablero.dimensiones[0]):
        for id_columna in range(tablero.dimensiones[1]):
            # si la celda es parte de esa columna, la añadimos a la lista
            if id_columna == columna:
                celda = tablero.tablero[id_fila][id_columna]
                lista.append(celda)

    return lista


def get_diagonal(tablero, fila: int, columna: int, prin: bool = True) -> tuple:
    """
    Dado un tablero, el numero de una fila y el de una columna, retorna una tupla, cuyo primer
    elemento es una lista unidimensional que por defecto representa a una diagonal (la de arriba
    hacia abajo) en la que esta ubicada una celda en la posicion (fila, columna).

    Si princ se asigna a False, se retorna la diagonal inversa (la de abajo hacia arriba)-

    El segundo elemento de la tupla es la posicion relativa de la celda en la posicion
    (fila, columna). Por ejemplo, si la celda es el tercer elemento de la diagonal, se retorna 3,
    esto se hace para no perder la referencia de la celda en la posicion (fila, columna)
    """
    lista = []
    # nuestra posicion de referencia de la celda respecto a su diagonal
    posicion_de_interes = 0
    contador_de_elementos = 0

    for id_fila in range(tablero.dimensiones[0]):
        for id_columna in range(tablero.dimensiones[1]):
            celda = tablero.tablero[id_fila][id_columna]

            # verificamos si la celda es la bomba que estamos analizando
            if (id_fila, id_columna) == (fila, columna):
                posicion_de_interes = contador_de_elementos

            # si estamos viendo la diagonal de abajo hacia arriba
            if prin:
                if (fila - columna) == (id_fila - id_columna):
                    lista.append(celda)
                    contador_de_elementos += 1

            # si estamos viendo la diagonal de arriba hacia abajo
            else:
                if (fila + columna) == (id_fila + id_columna):
                    lista.append(celda)
                    contador_de_elementos += 1

    return lista, posicion_de_interes


def alcance_horizontal(lista: int, posicion_interes: int) -> int:
    """
    Funcion que generaliza la busqueda de celdas_afectadas por la explosion de una bomba

    Recibe una lista que puede representar una fila, una columna, o una diagonal.
    En el caso de que se este viendo una bomba H, se puede ingresar una lista que represente una
    fila directamente. En el caso de que se este viendo una bomba V o R, es
    deber del metodo celdas_afectadas convertir la columna/diagonal a una lista unidimensional
    previo al llamado de esta funcion.

    Dada una lista y la posicion de interes (posicion de la celda explosiva
    respecto a su fila/columa/diagonal). Se itera sobre la lista, manteniendo un contador sobre
    que posicion vamos, y sumando celdas a medida que vayamos pasando, luego si nos topamos con una
    celda PP ANTES de pasar por la posicion de interes. Se resta todas las celdas que habiamos
    sumado, es decir, empezamos desde 0 la suma nuevamente.

    Pasada esta celda PP, volvemos a sumar las celdas que vayamos pasando. Con un bool, apuntamos si
    pasamos la posicion de interes, seguimos sumando y si nos hallamos con otra celda PP, detenemos
    el conteo, ya que no queremos seguir sumando las bombas que vienen despues de esa celda PP.

    La suma que nos quedaria seria el numero de celdas afectadas por esa bomba en la posicion de
    interes

    Ejemplo ¿Que ocurriria en este caso? [--, PP, --, --, PP, --, --, V2 ]
    Al ir iterando por la parte izquierda, cada vez que nos encontremos con una PP, se reinicia la
    suma a 0
    """
    paso_posicion_interes = False
    suma_celdas = 0
    contador_posicion = 0

    for celda in lista:

        if contador_posicion == posicion_interes:
            paso_posicion_interes = True
            # sumamos el paso por la posicion de interes y seguimos a la siguiente posicion
            suma_celdas += 1
            contador_posicion += 1
            continue

        # si ya pasamos por posicion_interes, entonces estamos por la derecha de la lista
        if paso_posicion_interes:
            # si la celda es PP, podemos deternos
            if celda == "PP":
                break

            # si la celda no es PP la sumamos
            else:
                suma_celdas += 1

            contador_posicion += 1

        # si aun no pasamos por la posicion de interes, entonces estamos por la izquierda de la
        # lista
        else:
            # si la celda es PP, reiniciamos la suma
            if celda == "PP":
                suma_celdas = 0

            # si la celda no es PP la sumamos
            else:
                suma_celdas += 1

            contador_posicion += 1

    return suma_celdas


def get_piezas_explosivas(tablero) -> list:
    """
    Retorna una lista con las posiciones de las piezas explosivas. Se iterea sobre las posiciones
    de la lista de listas y se van añadiendo celdas que no son celdas vacias, ni PPs
    """
    lista_piezas_explosivas = []
    for id_fila in range(tablero.dimensiones[0]):
        for id_columna in range(tablero.dimensiones[1]):
            celda = tablero.tablero[id_fila][id_columna]
            if celda != "--" and celda != "PP":
                lista_piezas_explosivas.append([id_fila, id_columna])
    return lista_piezas_explosivas  # lista de posiciones


if __name__ == "__main__":
    pass
