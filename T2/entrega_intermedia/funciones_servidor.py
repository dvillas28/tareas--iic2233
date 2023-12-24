from utils.utils_servidor import generador_secuencia


def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    """
    Revisa si el nombre de usuario no este en la lista de los usuarios no permitidos
    """

    return not (nombre in usuarios_no_permitidos)


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


if __name__ == "__main__":
    mensaje = bytearray(b"\x05\x08\x03\x02\x04\x03\x05\x07\x05\x06\x01")
    array = separar_mensaje(mensaje)
    for a in array:
        print(a)

    print(encriptar_mensaje(mensaje))
