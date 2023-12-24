from copy import copy
from pieza_explosiva import PiezaExplosiva
from misc_functions import (archivo_a_lista,
                            get_id_tablero,
                            crear_tablero)

from tablero_functions import (get_peones_invalidos,
                               get_columna,
                               get_diagonal,
                               alcance_horizontal)

from solver import (get_celdas_vacias,
                    solver_recursivo)


class Tablero:
    """
    Clase que representa al tablero. Se registra al tablero como lista de listas de strings
    """

    # NO MODIFICAR
    def __init__(self, tablero: list) -> None:
        # filas         #columnas
        self.dimensiones = [len(tablero), len(tablero[0])]
        self.tablero = tablero

    @property
    def desglose(self) -> list:
        """
        Property que retorna una lista con el numero de de piezas_exp, peones y celdas vacias
        - Utiliza al self.tablero
        """
        piezas_explosivas = 0
        peones = 0
        celdas_vacias = 0

        # itera sobre filas
        for i in range(self.dimensiones[0]):
            # itera sobre columnas
            for j in range(self.dimensiones[1]):

                celda = self.tablero[i][j]

                if celda[0] == "V" or celda[0] == "H" or celda[0] == "R":
                    piezas_explosivas += 1

                elif celda == "PP":
                    peones += 1

                elif celda == "--":
                    celdas_vacias += 1

        return [piezas_explosivas, peones, celdas_vacias]

    @property
    def peones_invalidos(self) -> int:
        """
        Property que retorna la cantidad de peones que no cumplen la REGLA 3
        REGLA 3: Un PP solo puede tener un PP vecino, un vecino es una celda al lado verticalmente
        o horizontalmente, no en diagonal.
        """
        peones_invalidos = get_peones_invalidos(self)
        return peones_invalidos

    @property
    def piezas_explosivas_invalidas(self) -> int:
        """
        Property que cuenta la cantidad de piezas explosivas no validas para el tablero
        - Una pieza explosiva no es valida si:
            cantidad_de_celdas_a_destruir > pieza.alcance (alcance maximo de la pieza)
        - IMPORTANTE: para calcular el alcance maximo, se ignora la existencia de los peones
        - Utiliza al self.tablero
        """
        piezas_exp_invalidas = 0
        # iteramos por el tablero hasta que encontremos una pieza explosiva
        for id_fila in range(self.dimensiones[0]):
            for id_columna in range(self.dimensiones[1]):
                celda = self.tablero[id_fila][id_columna]

                if celda[0] in "VHR":
                    # if isinstance(celda, PiezaExplosiva):
                    alcance_maximo = 0
                    tipo = celda[0]
                    # tipo = celda.tipo
                    celdas_a_destruir = int(celda[1:])
                    # celdas_a_destruir = int(celda.alcance)

                    # Pieza_Explosiva auxiliar para usar su metodo
                    cell = PiezaExplosiva(celdas_a_destruir, tipo, [
                                          id_fila, id_columna])
                    for i in range(self.dimensiones[0]):
                        for j in range(self.dimensiones[1]):
                            if cell.verificar_alcance(i, j):
                                alcance_maximo += 1

                    if celdas_a_destruir > alcance_maximo:
                        piezas_exp_invalidas += 1

        return piezas_exp_invalidas

    @property
    def tablero_transformado(self) -> list:
        """
        Property que retorna un nuevo tablerotablero (self.tablero), pero cada pieza explosiva es
        reemplaza por una instancia de PiezaExplosiva con la info acorde
        """
        tab_transformado = self.tablero.copy()

        for i in range(self.dimensiones[0]):
            for j in range(self.dimensiones[1]):
                celda = self.tablero[i][j]

                if celda[0] == "V" or celda[0] == "H" or celda[0] == "R":
                    tab_transformado[i][j] = PiezaExplosiva(
                        int(celda[1]), celda[0], [i, j])

        return tab_transformado

    def celdas_afectadas(self, fila: int, columna: int) -> int:
        """
        Dada una posicion, retorna el numero de celdas afectadas por la explosion de esa pieza
        Una celda afectada por la explosion si esta en la misma fila, columna o diagonal (segun el
        tipo), y que no exista un peon entre la pieza explosiva y la celda a destruir
        """
        # si el tablero no tiene una pieza explosiva, retornar -1
        celda = self.tablero[fila][columna]
        if celda == "PP" or celda == "--":
            return -1

        else:
            # la celda es una pieza explosiva
            tipo = celda[0]

            if tipo == "V":
                # crearemos una lista que representa las columna donde actua la bomba V
                lista_columna = get_columna(self, columna)
                celdas_afectadas = alcance_horizontal(lista_columna, fila)

            elif tipo == "H":
                # extraemos la lista de fila directamente del tablero
                lista_fila = self.tablero[fila]
                celdas_afectadas = alcance_horizontal(lista_fila, columna)

            # si es R debemos tomar la fila, la columna, las dos diagonales
            elif tipo == "R":

                lista_fila = self.tablero[fila]

                lista_columna = get_columna(self, columna)

                lista_diag1, pos_de_interes_diag1 = get_diagonal(
                    self, fila, columna)

                lista_diag2, pos_de_interes_diag2 = get_diagonal(
                    self, fila, columna, prin=False)

                # tomamos todos los alcances de las 4 listas
                celdas_afectadas_fila = alcance_horizontal(lista_fila, columna)
                celdas_afectadas_columna = alcance_horizontal(
                    lista_columna, fila)
                celdas_afectadas_diag1 = alcance_horizontal(
                    lista_diag1, pos_de_interes_diag1)
                celdas_afectadas_diag2 = alcance_horizontal(
                    lista_diag2, pos_de_interes_diag2)

                # le restamos 3 para no contar repeticiones por la celda_explosiva
                celdas_afectadas = celdas_afectadas_fila + celdas_afectadas_columna \
                    + celdas_afectadas_diag1 + celdas_afectadas_diag2 - 3

            return celdas_afectadas

    def limpiar(self) -> None:
        """
        Metodo que elimina los peones y los transforma en --
        """
        for id_fila in range(self.dimensiones[0]):
            for id_columna in range(self.dimensiones[1]):

                celda = self.tablero[id_fila][id_columna]
                if celda == "PP":
                    self.tablero[id_fila][id_columna] = "--"

    def reemplazar(self, nombre_nuevo_tablero: str) -> bool:
        """
        -utiliza tableros.txt, extrae la info del nombre indicado, y actualiaz los atributos
        de la instancia de Tablero (tablero y dimensiones), almacenar como una lista de listas
        """
        tableros = archivo_a_lista()
        tablero_id = get_id_tablero(nombre_nuevo_tablero, tableros)

        if tablero_id != -1:
            # el nuevo tablero existe
            nuevo_tablero = crear_tablero(tableros[tablero_id])
            self.tablero = nuevo_tablero
            self.dimensiones = [len(nuevo_tablero), len(nuevo_tablero[0])]
            return True

        return False

    def solucionar(self) -> list:
        """
        Soluciona al tablero.
        Se colocan peones de modo que cada pieza explosiva cumpla REGLA1, REGLA2 y REGLA3
        Si ya se incluyen peones no retirar ni mover
        retornar el nuevo tablero, no modificar el original, si tiene sol, retornar []
        """
        copia_aux = copy(self.tablero)

        celdas_criticas = get_celdas_vacias(self)
        soluciones = solver_recursivo(self, 0, celdas_criticas)

        # como el solver_recursivo manipulo al atrbiuto tablero, lo retornamos a
        # como estaba antes
        self.tablero = copy(copia_aux)

        # si no teneomos solucion, tenemos solo una lista vacia
        if soluciones == []:
            return soluciones

        return soluciones[0]


# testeos
if __name__ == "__main__":
    pass
