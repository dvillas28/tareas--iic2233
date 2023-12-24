from PyQt6.QtCore import pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap
from backend.logica_utils import parametros as p
from backend.logica_utils.funciones_jugador import generador_secuencia
from backend.logica_utils.entity import Entity
from random import choice


class Lobo(Entity):
    identificador = 0
    current_ponderador = p.PONDERADOR_LABERINTO_1

    def __init__(self,
                 primary_key: str,
                 tipo: str,
                 initial_pos: tuple,
                 spd: int,
                 senal_spawn: pyqtSignal,
                 senal_move: pyqtSignal,
                 senal_actualizar_pos: pyqtSignal,
                 senal_killed: pyqtSignal,
                 senal_frezzed: pyqtSignal,
                 status: str = 'not frezzed',
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.identificador = Lobo.identificador
        Lobo.identificador += 1

        # self.pixmaps: dict = pixmaps  # sus imagenes
        self.primary_key = primary_key

        self.tipo = tipo  # eje de movimiento del lobo
        self.initial_pos: tuple = initial_pos
        self.spd = spd

        # senales
        self.senal_spawn = senal_spawn
        self.senal_move = senal_move
        self.senal_actualizar_pos = senal_actualizar_pos
        self.senal_killed = senal_killed
        self.senal_freezed = senal_frezzed

        self.status = status

        # bools de movimiento
        self.moving: bool = False
        self.paused: bool = False
        self.frezzed: bool = False

        # mapas
        self.mapa: dict = None  # necesario para el movimiento

        # posicion interna
        self.current_position: list = None

        # posicion en cordenadas de tabla
        self.current_position_tab: list = None

        # direccion actual de movimiento
        self.current_dir: int = 1

        # pixmap
        self.current_pixmap_key: str = None

        # generador de secuencia para los indices del pixmap
        self.generador = generador_secuencia()

        # diccionario de direcciones, seran seteados al self.current dir
        self.direccion = {'H': ['L', 'R'],
                          'V': ['U', 'D']}

        self.direcciones = {'H': {-1: 'L', 1: 'R'},
                            'V': {-1: 'U', 1: 'D'}
                            }

        # metodos que utilizan los timers
        self.timer_data = {'H': [self.x_tab, 0],
                           'V': [self.y_tab, 1]}

        # timers activos
        self.active_timers = {}

        self.spd_based_on_status = {'not frezzed': round(1000/(self.spd * p.TAMAÑO_BLOQUE)),
                                    'frezzed': round(
                                        1000/(self.spd * p.TAMAÑO_BLOQUE *
                                              (1 - p.REDUCCION_VELOCIDAD)))}

    def spawn(self) -> None:
        """
        Coloca a los lobos en la posicion inicial
        """
        x = self.initial_pos[0]
        y = self.initial_pos[1]

        self.current_position = [x, y]
        self.current_position_tab = [self.x_tab(x), self.y_tab(y)]

        # seteamos un pixmap por defecto
        self.current_pixmap_key = f'L{self.tipo}_{choice(self.direccion[self.tipo])}_1'

        # de momento colocaremos un pixmap predeterminado
        self.senal_spawn.emit(
            self.current_position_tab,
            p.TAMAÑO_BLOQUE,
            self.current_pixmap_key,
            self.tipo,
            self.identificador
        )

    def move(self) -> None:
        """
        Crea el timer de animacion de posicion
        """

        x = self.current_position[0]
        y = self.current_position[1]

        self.current_position_tab = [self.x_tab(x), self.y_tab(y)]

        # print(round(1000/(p.VELOCIDAD_LOBO * p.TAMAÑO_BLOQUE * self.current_ponderador)))

        self.timer = QTimer()

        if self.status == 'frezzed':
            self.frezzed = True

        self.timer.setInterval(self.spd_based_on_status[self.status])
        # print(self.spd_based_on_status[self.status])
        # self.timer.timeout.connect(self.timer_methods[self.tipo])
        self.timer.timeout.connect(self.animated_move)

        self.active_timers['movement'] = self.timer

        self.timer.start()

    def animated_move(self) -> None:
        """
        Animacion de movimiento de una casilla a otra

        Cuando se llega a la otra casilla se verifica si es la pared, si es que si se cambia de
        direccion
        """
        # en base al tipo, tomamos la funcion (x_tab o y_tab) y el indice q se debe cambiar
        coord_func = self.timer_data[self.tipo][0]
        coord_index = self.timer_data[self.tipo][1]

        # calculamos la posicion en tablero de la siguente casilla
        coord_final = coord_func(
            self.current_position[coord_index] + (1 * self.current_dir))

        # si no estams en esa posicion
        if coord_final != self.current_position_tab[coord_index]:

            # nos movemos un pixel a esa casilla
            self.current_position_tab[coord_index] += (1 * self.current_dir)

            # actualizamos el pixmap
            self.current_pixmap_key = self.change_pixmap(self.current_dir)

            # emision al front end
            self.senal_move.emit(
                self.current_position_tab,
                self.current_pixmap_key,
                self.tipo,
                self.identificador
            )

            # emitir posicion al dict global
            self.senal_actualizar_pos.emit(self, self.current_position_tab)

        # se llego a la posicion animadamente
        elif coord_final == self.current_position_tab[coord_index]:
            # actualizar posicion interna
            self.current_position[coord_index] += (1 * self.current_dir)

            # calculamos la posicion siguente
            next_pos = self.current_position.copy()
            next_pos[coord_index] += (1 * self.current_dir)

            # consultamos si nos podemos mover a esa posicion
            if self.mapa.get(tuple(next_pos), None) == 'P':
                # cambiamos de direccion
                self.current_dir *= -1
                self.current_pixmap_key = self.change_pixmap(self.current_dir)
                # y emitimos la posicion de nuevo con el label actualizado

                self.senal_move.emit(
                    self.current_position_tab,
                    self.current_pixmap_key,
                    self.tipo,
                    self.identificador)

            elif self.mapa.get(tuple(next_pos), None) == 'EX':
                print(f'Lobo {self.identificador} quemado!')
                self.senal_killed.emit(self)
                self.timer.stop()

            elif self.mapa.get(tuple(next_pos), None) == 'CO' and not self.frezzed:
                print(f'Lobo {self.identificador} congelado!')
                self.timer.setInterval(self.spd_based_on_status['frezzed'])
                self.frezzed = True
                self.senal_freezed.emit(self.identificador)

    def change_pixmap(self, current_dir: int) -> str:

        i = next(self.generador)

        if self.tipo == 'H':
            if self.current_position_tab[0] % p.PIXELS_CAMBIO_PIXMAP == 0:
                tipo = f'L{self.tipo}_{self.direcciones[self.tipo][current_dir]}_{i}'

                return tipo

            return self.current_pixmap_key

        elif self.tipo == 'V':
            if self.current_position_tab[1] % p.PIXELS_CAMBIO_PIXMAP == 0:
                tipo = f'L{self.tipo}_{self.direcciones[self.tipo][current_dir]}_{i}'

                return tipo

            return self.current_pixmap_key

    def pause(self) -> None:

        if self.paused:
            self.paused = False
            self.move()
        else:

            if self.active_timers.get('movement', None) is not None:
                self.active_timers['movement'].stop()

            self.moving = False
            self.paused = True

    def get_current_spd(self, spd) -> int:
        self.current_spd = spd
