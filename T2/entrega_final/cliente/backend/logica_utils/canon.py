from backend.logica_utils import parametros as p
from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from backend.logica_utils.zanahoria import Zanahoria


class Canon(QObject):
    def __init__(self,
                 primary_key: str,
                 tipo: str,
                 pos: list,
                 senal_create_z_obj: pyqtSignal,
                 senal_spawn_z: pyqtSignal,
                 senal_move_z: pyqtSignal,
                 senal_kill_z: pyqtSignal,
                 senal_actualizar_pos: pyqtSignal,
                 *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        # self.pixmaps = pixmaps
        self.primary_key = primary_key
        self.tipo = tipo
        self.pos = pos
        self.mapa: dict = None

        # senales que maneja el cañon
        self.senal_create_z = senal_create_z_obj

        # senales que manejan las zanahorias
        self.senal_spawn = senal_spawn_z
        self.senal_move_z = senal_move_z
        self.senal_kill_z = senal_kill_z
        self.senal_actualizar_z = senal_actualizar_pos

        # timer de gestion de disparo
        self.shooting_timer = QTimer()

        # cada 5 segundos
        self.shooting_timer.setInterval(p.SEGUNDOS_DISPARO * 1000)
        self.shooting_timer.timeout.connect(self.shoot)

        self.bullets: list = []

        # bools de movimiento
        self.moving: bool = False
        self.paused: bool = False

    @property
    def start_pos(self):
        """
        Posicion de inicio de la zanahoria
        """

        if self.tipo == 'U':
            return [self.pos[0], self.pos[1] - 1]

        elif self.tipo == 'D':
            return [self.pos[0], self.pos[1] + 1]

        elif self.tipo == 'R':
            return [self.pos[0] + 1, self.pos[1]]

        elif self.tipo == 'L':
            return [self.pos[0] - 1, self.pos[1]]

    def start_timer(self):
        self.shooting_timer.start()

    def shoot(self):
        # crea una zanahora en la posicion adyacente
        # la hace moverse

        # comprobamos si es que esta muerto este timer
        if self.mapa[tuple(self.pos)] == 'EX':
            self.shooting_timer.stop()

        z = Zanahoria(self.primary_key,
                      self.tipo,
                      self.start_pos,
                      self.mapa,
                      self.senal_spawn,
                      self.senal_move_z,
                      self.senal_actualizar_z,
                      self.senal_kill_z)

        # crear la entidad grafica con create_movable_label del front
        # se crea el objeto y se añade a su diccionario propio
        self.senal_create_z.emit(z.tipo, z.identificador, self.primary_key)

        # anadirla al diccionario de entidades posicion
        self.senal_actualizar_z.emit(z, z.current_position_tab)

        self.bullets.append(z)

        z.spawn()
        z.move()

    def pause(self):

        if self.paused:
            self.paused = False
            self.start_timer()

        else:
            self.shooting_timer.stop()
            self.moving = False
            self.paused = True
