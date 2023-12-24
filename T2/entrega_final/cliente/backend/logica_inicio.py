from PyQt6.QtCore import QObject, pyqtSignal
import backend.logica_utils.funciones_logica as fl


# se importa comenzando por backend ya que main.py esta ahi


class LogicaInicio(QObject):

    # señales backend - ventana_inicio
    senal_iniciar_ventana_inicio = pyqtSignal()
    senal_anadir_jugador_data = pyqtSignal(str, str, int)
    senal_mostrar_popup = pyqtSignal(str)
    senal_cerrar_ventana_por_desconexion = pyqtSignal(bool)
    senal_ocultar_inicio = pyqtSignal()

    # señales backend inicio -> backend juego
    senal_on_front_close = pyqtSignal()
    senal_enviar_data_al_server = pyqtSignal(str)

    # senales exlusiva para hacaer de puente ente logica-cliente-backend inicio
    # nombre, puntaje, nivel
    senal_send_game_data = pyqtSignal(str, int, float)
    senal_iniciar_juego = pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        print(f"> Backend: Iniciando objeto logico")

        self.banned = None

    def start_inicio(self) -> None:
        self.senal_iniciar_ventana_inicio.emit()

    def validar_nombre(self, nombre: str) -> None:
        if fl.validacion_formato(nombre):
            print(f"> Backend: {nombre} es un nombre valido")
            print(f"> Backend: Enviando {nombre} a cliente")

            self.senal_enviar_data_al_server.emit(f'verify;{nombre}')

        else:
            print("> Backend: Nombre Invalido")
            self.senal_mostrar_popup.emit('Ingresa un nombre valido')

    def salir_ventana_inicio(self) -> None:
        print(f"> Backend: Frontend Cerrado. Avisando a cliente")
        self.senal_on_front_close.emit()

    def cerrar_ventana_por_desconexion(self) -> None:
        # metodo ejecutado por señal del cliente cuando el server se desconecta
        self.senal_cerrar_ventana_por_desconexion.emit(True)

    def anadir_jugador_data(self, name: str, score: str, place: int) -> None:
        # metodo ejecutado por señal del cliente para mostrar el top5 de jugadores
        # print('> Logica_inicio; recibiendo dato de top5, remitiendo a ventana_inicio')
        self.senal_anadir_jugador_data.emit(name, score, place)

    def set_player_status(self, data: list) -> None:
        # metodo llamado por cliente
        result = data[0]
        if result == 'sucess':
            self.banned = False

            # cerrar la ventana de inicio
            self.senal_ocultar_inicio.emit()

            user_name = data[1][0]
            level = int(data[1][1])
            points = data[1][2]

            # senal de envio de datos
            self.senal_send_game_data.emit(user_name, level+1, points)

            # enviar la señal para abrir a la ventana de juego
            self.senal_iniciar_juego.emit()

        elif result == 'banned':
            self.banned = True
            self.senal_mostrar_popup.emit('Ese nombre esta baneado')
