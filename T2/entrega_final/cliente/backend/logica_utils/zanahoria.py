from PyQt6.QtCore import pyqtSignal, QTimer
from backend.logica_utils.entity import Entity
from backend.logica_utils import parametros as p


class Zanahoria(Entity):
    identificador = 0

    def __init__(self,
                 primary_key: str,
                 tipo: str,
                 start_pos: list,
                 mapa: dict,
                 senal_spawn: pyqtSignal,
                 senal_move: pyqtSignal,
                 senal_actualizar_pos,
                 senal_kill: pyqtSignal,
                 *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.identificador = Zanahoria.identificador
        Zanahoria.identificador += 1

        self.tipo = tipo

        # pixmaps
        # self.pixmaps = pixmaps
        self.primary_key = primary_key
        self.secondary_key = f'Z{self.tipo}'

        # posicion inicial, al lado del cañon
        self.start_pos: list = start_pos

        self.mapa = mapa

        self.current_position = start_pos
        self.current_position_tab: list = [
            self.x_tab(self.current_position[0]), self.y_tab(self.current_position[1])]

        # senales
        self.senal_move = senal_move
        self.senal_spawn = senal_spawn
        self.senal_actualizar_pos = senal_actualizar_pos
        self.senal_kill = senal_kill

        # bools de movimiento
        self.moving: bool = False
        self.paused: bool = False

        # metodo de transformacion, direccion, coordenada a cambiar

        self.timer_data = {'U': [self.y_tab, -1, 1],
                           'D': [self.y_tab, 1, 1],
                           'L': [self.x_tab, -1, 0],
                           'R': [self.x_tab, 1, 0]}

        self.active_timers: dict = {}

        self.killed: bool = False

    def spawn(self) -> None:
        """
        Coloca a la zanahoria en la posicion inicial
        """
        x = self.start_pos[0]
        y = self.start_pos[1]

        self.current_position = [x, y]
        self.current_position_tab = [self.x_tab(x), self.y_tab(y)]

        self.senal_spawn.emit(
            self.current_position_tab,
            p.TAMAÑO_BLOQUE,
            self.secondary_key,
            self.tipo,
            self.identificador
        )

    def move(self) -> None:
        """
        Crea el timer de animacion de posicion
        """

        self.timer = QTimer()
        self.timer.setInterval(
            round(1000/(p.VELOCIDAD_ZANAHORIA * p.TAMAÑO_BLOQUE)))
        # self.timer.timeout.connect(self.timer_methods[self.tipo][0])
        self.timer.timeout.connect(self.animated_move)

        # para poder pausarlo despues
        self.active_timers['movement'] = self.timer

        self.timer.start()

    def animated_move(self) -> None:
        """
        Animacion de movimiento de una casilla a otra

        Cuando se llega a la otra casilla se verifica si es la pared, si es que si se cambia de
        direccion
        """

        # cual funcion transformadora
        coord_func = self.timer_data[self.tipo][0]
        # cual direccion usar
        direction = self.timer_data[self.tipo][1]
        # cual es el indice q hay q cambiar
        coord_index = self.timer_data[self.tipo][2]

        # coordenada de la siguente casilla
        coord_final = coord_func(
            self.current_position[coord_index] + (1 * direction))

        # si no estamos en esa posicion
        if coord_final != self.current_position_tab[coord_index]:

            # nos movemos un pixel a esa casilla
            self.current_position_tab[coord_index] += (1 * direction)

            # emision al front end
            self.senal_move.emit(
                self.current_position_tab,
                self.secondary_key,
                self.tipo,
                self.identificador
            )

            # emitir posicion al dict global
            self.senal_actualizar_pos.emit(self, self.current_position_tab)

        # se llego a la posicion animadamente
        elif coord_final == self.current_position_tab[coord_index]:

            # actualizar posicion interna
            self.current_position[coord_index] += (1 * direction)

            # calculamos la posicion siguente
            next_pos = self.current_position.copy()
            next_pos[coord_index] += (1 * direction)

            # consultamos si nos podemos mover a esa posicion
            if self.mapa.get(tuple(next_pos), None) == 'P':
                self.timer.stop()
                # print(f'{self.identificador} golpee la pared!')
                self.senal_kill.emit(self)
                self.killed = True

            elif self.mapa.get(tuple(next_pos), None) == 'EX':
                self.timer.stop()
                self.senal_kill.emit(self)
                self.killed = True

    def pause(self) -> None:

        if self.paused and not self.killed:
            self.paused = False
            self.move()

        else:

            if self.active_timers.get('movement', None) is not None:
                self.active_timers['movement'].stop()

            self.moving = False
            self.paused = True
