from imprimir_tablero import imprimir_tablero
from misc_functions import (get_id_tablero,
                            crear_tablero)
from tablero import Tablero


def menu(user_name: str, tablero_name: str, tableros: list) -> None:
    """
    Flujo principal del programa. Aqui el usuario puede elegir que hacer con los tableros
    """

    # extraer el id del tablero. Para este punto esta comprobado que ya existe
    tablero_id = get_id_tablero(tablero_name, tableros)
    tablero_lista = crear_tablero(tableros[tablero_id])

    # instanciamos a la lista de lista del tablero como un Tablero
    tablero = Tablero(tablero_lista)

    # tablero.tablero_transformado

    menu = """*** Menú de Acciones ***\n
    [1] Mostrar tablero
    [2] Limpiar tablero
    [3] Solucionar tablero
    [4] Salir del programa
    """

    # inicio menu
    print(f"> Hola {user_name}!\n")
    print(menu)
    option = input("> Indique su opción (1, 2, 3 o 4):\n")

    while option != "4":
        if option == "1":
            print("> Mostrando tablero")
            imprimir_tablero(tablero.tablero)

        elif option == "2":
            print("> Limpiando tablero")
            tablero.limpiar()

        elif option == "3":
            print("> Tablero solucionado")
            sol = tablero.solucionar()
            if sol == []:
                print([])
            else:
                imprimir_tablero(sol)
        else:
            print("> Opción Inválida\n")

        print(menu)
        option = input("> Indique su opción (1, 2, 3 o 4):\n")

    if option == "4":
        print('> Saliendo')
