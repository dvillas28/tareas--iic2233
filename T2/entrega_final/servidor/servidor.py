import socket
import threading
import json
import os
import utils.funciones_servidor as fs  # funciones
from utils.mensaje import Mensaje
from utils.parametros_servidor import RUTA_BANEADOS, RUTA_PUNTAJES


class Servidor:

    # funciones para setear comunicacion server-clientes
    def __init__(self, port: str, host: str) -> None:
        print(f'> Bienvenido. Inicializando servidor...')

        self.host = host
        self.port = int(port)

        # locks para threading
        self.user_list_lock = threading.Lock()

        # lista de baneados
        self.banned_list = self.open_banned_list()

        # sockets de los jugadores
        self.sockets = {}

        # socket del server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # enlazamos y escuchamos
        self.bind_and_listen()

        # intanciamos al thread portero que acepta las conexiones
        self.accept_connections()

    def bind_and_listen(self) -> None:
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f'> Servidor enlazado a [{self.host}, puerto {self.port}]')

    def accept_connections(self) -> None:
        portero = threading.Thread(target=self.accept_connections_thread,
                                   daemon=True)
        portero.start()

    def accept_connections_thread(self) -> None:
        """
        Acepta la conexion y crea un thread trabajador que se encarga de gestionar el socket
        de ese cliente
        """
        print(f'> Servidor iniciado. Aceptando conexiones')

        while True:
            socket_cliente, direccion = self.socket.accept()
            print(f'\n> Cliente recibido desde {direccion}')
            worker = threading.Thread(target=self.listen_client_thread,
                                      daemon=True,
                                      args=(socket_cliente,))

            # luego almacenaremos el nombre
            self.sockets[socket_cliente] = [direccion, "USUARIO SIN REGISTRAR"]

            # envio de los archivos de guardado
            top = self.send_top()
            print('> Enviando top5 al cliente')
            self.send(f'top5;{json.dumps(top)}', socket_cliente)

            worker.start()

    # Funciones de intercambio de info servidor-cliente
    def send(self, message: str, socket_cliente: socket.socket) -> None:
        """
        Envia un mensaje desde un socket cliente. Primero lo encripta y luego lo envia
        """

        # PROCESO DE ENCRIPTACION Y CODIFICACION MENSAJE

        # print(f'Sevidor: encriptando <{message}>')

        msg_serializado = fs.serializar_mensaje(message)
        msg_encriptado = fs.encriptar_mensaje(msg_serializado)
        # [largo, 0, array0, 1, array1, 2, array2...]
        msg_codificado = fs.codificar_mensaje(msg_encriptado)

        # enviamos el largo
        socket_cliente.sendall(msg_codificado[0])

        # enviamos los bloques de bytes

        # print(f'> Servidor: encriptacion lista. Enviando {msg_codificado[1:]}')
        for array in msg_codificado[1:]:
            socket_cliente.sendall(array)

    def listen_client_thread(self, socket_cliente: socket.socket) -> None:
        """ Thread que trabaja con el cliente
        - Primero: enviarle al cliente el top 5 actual, el backend del cliente se
        encargara de gestionarlo
        """

        while True:

            # PROCESO DE DECODIFICACION BYTEARRAY

            # recibimos el largo del mensaje
            response_bytes_length = socket_cliente.recv(4)
            response_length = int.from_bytes(response_bytes_length, 'big')

            response_curr_len = 0
            response_blocks = list()
            c = 1

            # lectura por chunks
            while response_curr_len < response_length:
                if c % 2 != 0:
                    num_block = socket_cliente.recv(4)
                else:
                    block = socket_cliente.recv(36)

                    response_blocks.append(bytearray(block))
                    response_curr_len += len(block)

                c += 1

            if response_blocks:
                fs.quit_padding(response_blocks[-1])

                encripted_response = bytearray()

                for block in response_blocks:
                    encripted_response.extend(block)

                response = self.decrypt_msg(encripted_response)

                if response != "":  # no es un mensaje vacio
                    if not self.handle_msg(response, socket_cliente):
                        break

    def decrypt_msg(self, array: bytearray) -> str:
        """
        Decodifica el mensaje recibido
        """

        # PROCESO DE DESENCRIPTACION ARRAY

        # print(f'> Servidor: decodificando: {array}')
        if not array:
            return ''
        # return '<MENSAJE DECODIFICADO>'
        return fs.decrypt(array)

    def handle_msg(self, msg: str, socket_cliente: socket.socket) -> bool:
        """
        Funcion principal encargada de procesar la solicitudes del cliente
        """
        mensaje = Mensaje(*(msg.split(';')))

        half1 = "> Procesando solicitud de "
        half2 = f"<{mensaje.orden}> de {self.sockets[socket_cliente][1]}"

        # print(half1 + half2)

        # MANEJO SOLICITUDES DEL SERVER
        if mensaje.orden == 'disconnect':
            self.notificar_desconexion_socket(socket_cliente)
            return False

        elif mensaje.orden == 'verify':
            self.verificar_nombre_usuario(mensaje.contenido, socket_cliente)

        elif mensaje.orden == 'save':
            print('> Guardando datos del usuario')
            # guardar datos del usuario, usar un lock
            self.save_user_data(json.loads(mensaje.contenido))

        # si la solicitud no fue una desconexion, es porque seguimos desconectados
        # y es necesario que el thread lo sepa
        return True

    # funciones miscelaneas del servidor

    # FUNCIONES LECTORAS DE ARCHIVOS
    def open_banned_list(self) -> list:

        path = os.path.join(*(RUTA_BANEADOS.split('/')))
        with open(path, 'r') as file:
            banned_list = json.load(file)

        return banned_list

    def read_users_list(self) -> list:
        list_to_return = list()
        path = os.path.join(*(RUTA_PUNTAJES.split('/')))
        # como un thread abre un archivo, es seguro usar un lock
        self.user_list_lock.acquire()

        with open(path, 'r') as file:
            lineas = file.readlines()

        self.user_list_lock.release()

        for linea in lineas:
            linea = linea.strip().split(',')
            linea[1] = str(linea[1])
            linea[2] = str(linea[2])
            list_to_return.append(linea)
        return list_to_return

    def send_top(self) -> list:
        # abrir el archivo

        lista_top = self.read_users_list()

        lista_top.sort(key=lambda player: -1*float(player[2]))
        return lista_top[:5]

    # FUNCIONES EJECUTADAS POR HANDLE
    def notificar_desconexion_socket(self, socket_cliente: socket.socket) -> None:
        print(f'> {self.sockets[socket_cliente][1]} se ha desconectado')
        self.sockets.pop(socket_cliente)

    def verificar_lista_baneados(self, nombre: str) -> str:

        if fs.usuario_permitido(nombre, self.banned_list):
            result = 'sucess'

        else:
            result = 'banned'
            print(f'> Usuario baneado {nombre} tratando de ingresar')

        return result

    def buscar_usuario(self, name: str) -> list:
        # funcion que busca la existencia del usuario y prepara el paquete de datos
        # a enviar

        lista_top = self.read_users_list()

        for user in lista_top:
            if name == user[0]:
                print(f'> Datos de usuario {name} encontrados')

                level = user[1]
                points = float(user[2])
                data = ['sucess', [name, level, points]]

                return data

        # el usuario no existia antes
        print(f'> Usuario {name} registrado')
        data = ['sucess', [name, 0, 0]]

        return data

    def verificar_nombre_usuario(self, contenido: str, socket_cliente: socket.socket) -> None:

        result = self.verificar_lista_baneados(contenido)

        data = [result, []]  # envio por default

        if result == 'sucess':
            # [result, [name, level, points]]
            data = self.buscar_usuario(contenido)
            self.sockets[socket_cliente][1] = contenido

        # enviamos la respuesta con los datos en formato json
        self.send(f'verify;{json.dumps(data)}', socket_cliente)

    def save_user_data(self, data: list) -> None:
        lista_usuarios = self.read_users_list().copy()
        status = data[0]
        user_name = data[1]
        level = data[2]
        points = data[3]

        if int(level) == 4:
            lvl_to_display = int(level) - 1
        else:
            lvl_to_display = int(level)

        print(
            f'> Usuario {user_name} {status} nivel {lvl_to_display}. Puntaje actual {points}')

        if user_name in [user[0] for user in lista_usuarios]:
            # si el puntaje recibido es mayor al puntaje registrado, guardarlo, si no ignorarlo

            for user in lista_usuarios:
                if user_name == user[0]:
                    # if user_name == user[0] and float(points) > float(user[2]):
                    # overwrite files
                    # print(
                    #     f'> {user_name} supero su record! ({user[2]} -> {points})')
                    user[0] = user_name
                    user[1] = level
                    user[2] = points

        else:
            lista_usuarios.append([user_name, level, points])

        self.overwrite_users_list(lista_usuarios)

    def overwrite_users_list(self, lista_usuarios: list) -> None:
        print('\n> Sobreescribiendo base de datos. No apagues el servidor')

        path = os.path.join(*(RUTA_PUNTAJES.split('/')))

        self.user_list_lock.acquire()

        with open(path, 'w') as arch:

            for user in lista_usuarios:
                user_name = user[0]
                level = user[1]
                points = user[2]

                if user == lista_usuarios[-1]:
                    arch.write(f'{user_name},{level},{points}')
                else:
                    arch.write(f'{user_name},{level},{points}\n')

        self.user_list_lock.release()

        print('> Guardado Listo')

    # FUNCIONES MISCELANEAS

    def desconectar_sockets(self) -> None:
        for socket in list(self.sockets.keys()):
            try:
                self.send('connection lost;_', socket)
                print(f'> Usuario {self.sockets[socket][1]} desconectado')
                socket.close()

            except BrokenPipeError:
                # si nos topamos con un socket de un
                # usuario que ya se desconecto, no hacemos nada
                pass

        self.socket.close()


if __name__ == "__main__":
    print("Clase Servidor. Porfavor, ejecuta el archivo main.py para inicializar servidor")
