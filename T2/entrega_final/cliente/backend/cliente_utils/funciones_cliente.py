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


def serializar_mensaje(mensaje: str) -> bytearray:
    return bytearray(mensaje.encode("utf-8"))


def separar_mensaje(mensaje: bytearray) -> list[bytearray]:
    A = bytearray()
    B = bytearray()
    C = bytearray()

    generador = generador_secuencia(A, B, C)

    for i in range(len(mensaje)):
        byte = mensaje[i:i+1]
        array = next(generador)
        array.extend(byte)

    return [A, B, C]


def encriptar_mensaje(mensaje: bytearray) -> bytearray:
    mensaje_encriptado = bytearray()

    mensaje_separado = separar_mensaje(mensaje)
    A = mensaje_separado[0]
    B = mensaje_separado[1]
    C = mensaje_separado[2]

    n1 = A[0]  # primer byte
    n2 = B[-1]  # ultimo byte
    n3 = C[0]  # primer byte

    suma = n1 + n2 + n3

    if suma % 2 == 0:
        mensaje_encriptado.extend(b'1' + A + C + B)

    else:
        mensaje_encriptado.extend(b'0' + B + A + C)

    return mensaje_encriptado


def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:
    lista_codificada = []

    largo = len(mensaje)
    largo_bytes = bytearray(largo.to_bytes(4, "big"))
    lista_codificada.append(largo_bytes)

    contador = 1

    for i in range(0, len(mensaje), 36):
        chunk = mensaje[i:i+36]
        if len(chunk) < 36:
            diferencia = 36 - len(chunk)
            # agregamos la diferencia en bytes 0
            for _ in range(diferencia):
                chunk.extend(b'\x00')

        numero_bloque = bytearray(contador.to_bytes(4, 'big'))
        lista_codificada.append(numero_bloque)
        lista_codificada.append(chunk)

        contador += 1

    return lista_codificada


def quit_padding(array: bytearray) -> None:
    """Le quita los ceros al array """

    # print('quitting padding')
    while array and array[-1] == 0:
        array.pop()


def which_is_different(list_of_arrays: list[bytearray]) -> int:
    """
    Retorna el array con largo distinto a los otros dos y su posicion.
    Si los 3 son del mismo largo se retorna -1
    """

    A = list_of_arrays[0]
    B = list_of_arrays[1]
    C = list_of_arrays[2]

    if len(A) == len(B) == len(C):
        return -1

    elif len(A) == len(B):
        return 2

    elif len(A) == len(C):
        return 1

    elif len(B) == len(C):
        return 0


def decrypt(array: bytearray) -> str:
    """
    Desencripta el mensaje ya descodificado
    """
    orden = int(array[0:1].decode())

    array.pop(0)

    array_separado = separar_mensaje(array)

    _A = array_separado[0]
    _B = array_separado[1]
    _C = array_separado[2]

    list_of_arrays = [_A, _B, _C]

    # tomamos el array con largo disinto y su posicion actual
    index = which_is_different(list_of_arrays)

    if index == -1:
        # todos los bloques son del mismo largo
        lista_arrays_mismo_largo = list()
        largo = len(_A)  # cualquiera sirve

        for i in range(0, len(array), largo):
            slice = array[i:i+largo]
            lista_arrays_mismo_largo.append(slice)

        # retornamos el mensaje a su orden original (ABC) en funcion del orden
        message_scrambled = return_to_og_order(orden, lista_arrays_mismo_largo)
        return unscramble(message_scrambled)

    else:
        # el valor del index nos indica cual es el mas largo
        if index == 0:
            # _A es el mas largo
            if orden == 0:
                B = array[:len(_B)]
                C = array[len(_A) + len(_B):]
                A = array[len(_B): len(_B) + len(_A)]

            elif orden == 1:
                A = array[:len(_A)]
                C, B = split_array_even(array[len(_A):])

        elif index == 1:
            # _B es el mas largo
            if orden == 0:
                B = array[:len(_B)]
                A, C = split_array_even(array[len(_B):])

            elif orden == 1:
                B = array[len(_B):]
                A, C = split_array_even(array[:len(_B)])

        elif index == 2:
            # _C es el mas largo
            if orden == 0:
                C = array[len(_A) + len(_B):]
                B, A = split_array_even(array[:len(_A) + len(_B)])

            elif orden == 1:
                A = array[:len(_A)]
                B = array[len(_C) + len(_A):]
                C = array[len(_A): len(_C) + len(_A)]

        # message_scrambled = return_to_og_order(orden, [A, B, C])
        # print(message_scrambled)

    # ahora reordenamos el mensaje
    message = unscramble([A, B, C])

    return message


def return_to_og_order(disposicion: int, list_of_arrays: list[bytearray]) -> list:
    """
    Reoredena los arrays en funcion de la disposicion en la que se encontraban encriptados
    """

    subarray1 = list_of_arrays[0]
    subarray2 = list_of_arrays[1]
    subarray3 = list_of_arrays[2]

    # print(subarray1)
    # print(subarray2)
    # print(subarray3)

    # print(disposicion)
    if disposicion == 0:
        original_order = [subarray2, subarray1, subarray3]

    elif disposicion == 1:

        original_order = [subarray1, subarray3, subarray2]

    return original_order


def unscramble(list_of_arrays: list[bytearray]) -> str:
    A = list_of_arrays[0]
    B = list_of_arrays[1]
    C = list_of_arrays[2]

    # print(A)
    # print(B)
    # print(C)

    scrambled_msg = bytearray(A + B + C)

    message = bytearray()

    generador = generador_secuencia(A, B, C)

    for _ in range(len(scrambled_msg)):
        array = next(generador)

        byte = array[0:1]

        if array:
            array.pop(0)

        message.extend(byte)

    return message.decode()


def split_array_even(array: list[Any]) -> tuple[Any]:
    """
    Dado el largo del array lo separa en dos partes del mismo largo
    """
    # print(array)
    first_array = bytearray(array[:len(array)//2])
    second_array = bytearray(array[len(array)//2:])

    return first_array, second_array
