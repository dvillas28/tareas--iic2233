import sys
from menu import menu
from misc_functions import (archivo_a_lista,
                            ingresar_datos)


# TODO: modularizar la primera parte de este codigo
def main() -> None:
    user_name, tablero_name = sys.argv[1], sys.argv[2]

    # cargamos la base de datos de tableros
    tableros = archivo_a_lista()

    # se comprueba si se puede ingresar al menu
    puede_ingresar = ingresar_datos(user_name, tablero_name, tableros)

    if puede_ingresar:

        menu(user_name, tablero_name, tableros)

    # si no puede ingresar, el programa termina


if __name__ == "__main__":
    main()
