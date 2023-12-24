from typing import Any


def generador_secuencia(A: Any, B: Any, C: Any) -> Any:
    """
    Genera una secuencia ABCCBAABC..., donde el tipo de los parametros no esta restringido
    Se retorna uno de los argumentos en funcion del puntero, luego se
    actualiza la direccion del puntero, y el nuevo puntero
    """

    puntero = 1  # 'puntero' de cual parametro retornar
    multi = 1  # determina la direccion a a la que se mueve el puntero

    while True:
        if puntero == 1:
            yield A

            if multi == -1:
                multi = 1

            elif multi == 1:
                puntero += 1 * multi

        elif puntero == 2:
            yield B

            puntero += 1 * multi

        elif puntero == 3:
            yield C

            if multi == 1:
                multi = -1

            elif multi == -1:
                puntero += 1 * multi


if __name__ == "__main__":
    x = generador_secuencia("A", "B", "C")
    for i in range(15):
        print(next(x))
