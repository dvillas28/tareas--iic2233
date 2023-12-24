from PyQt6.QtCore import QObject, pyqtSignal  # comunicacion backend-cliente
import backend.cliente_utils.funciones_cliente as fc
from backend.cliente_utils.mensaje import Mensaje
import socket
import json
import threading
from time import sleep


class Cliente(QObject):
    """
    Clase gestora del socket del cliente y la comunicacion del server
    - objeto logico de pyqt6 que puede comunicarse con el backend a traves de señales
    con el objetivo de hacer el traspaso de datos, que despues seran encriptados y enviados
    al servidor. Tambien viceversa
    """
    # señales para el backend logico del inicio
    senal_cerrar_ventana_por_desconexion = pyqtSignal()
    senal_enviar_jugador_data = pyqtSignal(str, str, int)
    senal_enviar_player_status = pyqtSignal(list)

    # funciones para setear comunicacion cliente-server
    def __init__(self, port: int,
                 host: str,
                 logica_inicio: QObject,
                 logica_juego: QObject,
                 *args,
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.port = port
        self.host = host
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente_highscore: int = None

        # backend. envia los mensajes al backend
        self.logica_inicio = logica_inicio
        self.logica_juego = logica_juego

        self.front_open = True

        try:
            self.connect_to_server()  # conectar al servidor
            self.listen()  # escuchar al servidor

        except ConnectionError:
            print(
                f"> Cliente Error: No se ha podido establecer conexion con servidor {self.host}")
            self.socket_cliente.close()
            self.conectado = False
            exit()

    def connect_to_server(self) -> None:
        self.socket_cliente.connect((self.host, self.port))
        print("> Cliente: conectado exitosamente al servidor")
        self.conectado = True

    def listen(self) -> None:
        """
        Inicializa el thread que escucha mensajes del servidor
        """

        thread = threading.Thread(target=self.listen_thread, daemon=True)
        thread.start()

# Funciones de intercambio de info entre servidor-cliente
    def send(self, msg: str) -> None:
        """
        Envia un mensaje al servidor
        """
        # PROCESO DE ENRCIPTACION Y CODIFICACION MENSAJE

        # print(f"> Cliente: encriptando {msg}")

        msg_serializado = fc.serializar_mensaje(msg)
        msg_encriptado = fc.encriptar_mensaje(msg_serializado)

        msg_codificado = fc.codificar_mensaje(msg_encriptado)

        # enviamos el largo
        self.socket_cliente.sendall(msg_codificado[0])

        # envio de bloque de bytes
        # print(f"> Cliente: enciptacion lista. Enviando {msg_codificado[1:]}")
        for array in msg_codificado[1:]:
            try:
                self.socket_cliente.sendall(array)
            except BrokenPipeError:
                print('> Error: Servidor cerrado durante ejecucion')
                self.socket_cliente.close()
                break

    def listen_thread(self) -> None:

        # print('> Thread Listener: manteniendo intercambio de informacion')
        try:
            while self.conectado:

                # PROCESO DE DECODIFICACION BYTEARRAY

                # recibimos el largo del mensaje
                response_bytes_length = self.socket_cliente.recv(4)
                response_len = int.from_bytes(response_bytes_length, 'big')
                # print(f'Largo del mensaje recibido: {response_len}')

                # iremos armando al bloque del mensaje
                response_curr_len = 0
                response_blocks = list()
                c = 1
                # mientras el mensaje no sea del largo recibido
                while response_curr_len < response_len:

                    if c % 2 != 0:
                        num_block = self.socket_cliente.recv(4)
                        # print(
                        # f'> Cliente: Recibido el bloque numero {int.from_bytes(num_block, "big")}')

                    else:
                        block = self.socket_cliente.recv(36)
                        # print(
                        # f'> Cliente: Recibido bloque {int.from_bytes(num_block, "big")}: {block}')
                        response_blocks.append(bytearray(block))
                        response_curr_len += len(block)

                    c += 1

                # si es que el mensaje no fue vacio, quitamos los bloques
                if response_blocks:
                    fc.quit_padding(response_blocks[-1])

                    encripted_response = bytearray()

                    for block in response_blocks:
                        encripted_response.extend(block)

                    response = self.decrypt_msg(encripted_response)

                    if response != "":  # no es un mensaje vacio

                        if not self.handle_msg(response):
                            break

        # este error solo aparece cuando el usuario de desconecta del servidor, cuando los programas
        #  se ejecutan en Win10 (ConectionAbortedError [WinError 10053])
        except ConnectionAbortedError:
            self.socket_cliente.close()

        except OSError:
            print(f'> Cerrando threads')
            self.senal_cerrar_ventana_por_desconexion.emit()
            self.socket_cliente.close()

    def decrypt_msg(self, array: bytearray) -> str:
        """
        Decodifica el mensaje recibido
        """

        # PROCESO DE DESENCRIPTACION ARRAY

        # print(f'> Cliente: decodificando: {array}')
        # si se recibio un vacio, retornar un vacio
        if not array:
            return ''

        return fc.decrypt(array)
###########################

    def handle_msg(self, msg: str) -> bool:
        """
        Funcion encargada de procesar mensajes del server
        """
        mensaje = Mensaje(*(msg.split(';')))

        print(f"> Cliente: Procesando <{mensaje.orden}> del servidor")

        if mensaje.orden == 'top5':
            # cargar el top 5
            # print(f'> Cliente:  Recibiendo Top5 del cliente')
            self.load_top5(json.loads(mensaje.contenido))
            # self.load_top5(json.loads(mensaje.contenido))

        elif mensaje.orden == 'verify':
            # enviar el resultado al backend
            data = json.loads(mensaje.contenido)
            player_status = data[0]
            player_stats: list = self.check_puntaje(data[1])
            self.senal_enviar_player_status.emit([player_status, player_stats])

        elif mensaje.orden == 'connection lost':
            # desconexion del servidor
            self.server_connection_lost()
            return False

        return True

    def load_top5(self, contenido: list) -> None:
        c = 1
        for user in contenido:
            # print('> Cliente: Emitiendo usuario top5 a logica_inicio')
            username = user[0]
            score = user[2]
            sleep(0.01)
            self.senal_enviar_jugador_data.emit(username, score, c)
            c += 1

    def server_connection_lost(self) -> None:
        print('> Cliente: Desconexion perdida con el servidor. Cerrando programa')
        self.senal_cerrar_ventana_por_desconexion.emit()
        self.conectado = False
        self.socket_cliente.close()

    def check_puntaje(self, contenido: list) -> list:
        if contenido:
            name = contenido[0]
            nivel = contenido[1]
            puntos = contenido[2]
            self.cliente_highscore = puntos
            if int(nivel) == 3:
                print(
                    f'> Cliente: Usuario ya completando el juego, cargando desde el principio')
                return [name, '0', puntos]
            return [name, nivel, puntos]
        else:
            return []

    # METODOS llamados desde señales del backend

    def on_front_close(self) -> None:
        """
        Funcion que se ejecuta cuando el frontend se cierra, con la X o el boton terminar
        Se deben realizar todas las acciones para cerrar al cliente y la logica
        """

        if self.conectado:
            print('> Cliente: Aviso recibido, desconectandose del servidor')

            try:
                self.send('disconnect;_')
            except OSError:
                print('Servidor desconectado durante ejecucion')
            finally:
                self.conectado = False
                self.socket_cliente.close()

        self.front_open = False

    def send_data_to_server(self, msg: str) -> None:
        # metodo conectado a una señal del backend. Envia info al server
        print(f"> Cliente: Enviando {msg} a servidor")
        self.send(msg)
