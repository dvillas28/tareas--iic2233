class PiezaExplosiva:
    """
    Clase que representa una pieza explosiva. Registra la cantidad de celdas que debe
    destruir esta pieza (alcance), (tipo) de pieza, y su (posicion) en el tablero
    """

    # NO MODIFICAR
    def __init__(self, alcance: int, tipo: str, posicion: list) -> None:
        self.alcance = alcance
        self.tipo = tipo
        self.posicion = posicion

    # NO MODIFICAR
    def __str__(self) -> str:
        fila, columna = self.posicion
        texto = f"Soy la pieza {self.tipo}{self.alcance}\n"
        texto += f"\tEstoy en la fila {fila} y columna {columna}\n"
        return texto

    def verificar_alcance(self, fila: int, columna: int) -> bool:
        """
        Verifica si la posicion (fila, columna) es parte de la
        explosion de una pieza explosiva. Se asume que fila, columa >= 0
        """
        # si es V
        if self.tipo == "V":
            if columna == self.posicion[1]:
                return True

        # si es H
        elif self.tipo == "H":
            if fila == self.posicion[0]:
                return True

        # si es R
        elif self.tipo == "R":
            misma_columna = columna == self.posicion[1]
            misma_fila = fila == self.posicion[0]

            # dos elementos estan en la misma diagonal principal cuando la resta de sus coordenadas
            # son iguales
            misma_diag_principal = (
                fila - columna) == (self.posicion[0] - self.posicion[1])

            # dos elementos estan en la misma diagonal principal cuando la suma de sus coordenadas
            # son iguales
            misma_diag_secundaria = (
                fila + columna) == (self.posicion[0] + self.posicion[1])

            if misma_columna or misma_fila or misma_diag_principal or misma_diag_secundaria:
                return True

        return False


if __name__ == "__main__":
    """
    Ejemplos:

    Dado el siguiente tablero
    [
        ["--", "V2", "PP", "--", "H2"],
        ["H3", "--", "--", "PP", "R11"]
    ]

    """
    # Ejemplo 1 - Pieza R11
    pieza_1 = PiezaExplosiva(11, "R", [1, 4])
    print(str(pieza_1))

    # Ejemplo 2 - Pieza V2
    pieza_2 = PiezaExplosiva(2, "V", [0, 1])
    print(str(pieza_2))
