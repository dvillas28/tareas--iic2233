from PyQt6.QtCore import pyqtSignal, QTimer
from backend.logica_utils.entity import Entity
from backend.logica_utils.funciones_jugador import (validar_direccion,
                                                    riesgo_mortal,
                                                    generador_secuencia)
from backend.logica_utils import parametros as p


class Player(Entity):
    def __init__(self,
                 primary_key: str,
                 senal_spawn: pyqtSignal,
                 senal_move: pyqtSignal,
                 senal_change_lvl: pyqtSignal,
                 senal_actualizar_pos: pyqtSignal,
                 senal_risk_colision: pyqtSignal,
                 senal_killed_by_ex: pyqtSignal,
                 *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # sus imagenes
        self.primary_key = primary_key

        # senales
        self.senal_spawn = senal_spawn
        self.senal_move = senal_move
        self.senal_change_lvl = senal_change_lvl
        self.senal_actualizar_pos = senal_actualizar_pos
        self.senal_risk_colision = senal_risk_colision
        self.senal_killed_by_ex = senal_killed_by_ex

        # bools de movimiento
        self.moving: bool = False
        self.paused: bool = False
        self.killed: bool = False
        self.frezzed: bool = False

        # Variables cuyo valor cambiara a medida que nos movamos y cambiemos de nivel
        # diccionario de posiciones
        self.mapa: dict = None
        self.laberinto: list[list] = None

        # posiciones inicio y final
        self.start_pos: list = None
        self.end_pos: list = None

        # posicion actual
        self.current_position: list = None

        # posicion actual en coordenadas de tabla
        self.current_position_tab: list = None

        # direccion positiva o negativa
        self.current_dir: int = None

        # pixmap actual
        self.current_pixmap_key: str = None

        # generador de secuencia para los pixmaps
        self.generador = generador_secuencia()

        # lista de objetos solidos
        self.walls = ['P', 'CU', 'CD', 'CL', 'CR']

        # metodos que utilizan los timers
        self.timer_methods = {'x': self.animated_move_h,
                              'y': self.animated_move_v}

        # timers activos
        self.active_timers: dict = {}

        # ultima tecla presionada
        self.last_key: str = None

        self.colision_timer = QTimer()
        self.colision_timer.setInterval(1)
        self.colision_timer.timeout.connect(self.check_collision)

    def spawn(self) -> None:
        """
        Coloca al jugador en la posicion inicial
        """
        self.killed = False
        self.paused = False

        x = self.start_pos[0]
        y = self.start_pos[1]

        # seteamos la variable interna
        self.current_position = [x, y]
        self.current_position_tab = [self.x_tab(x), self.y_tab(y)]

        self.senal_spawn.emit(
            self.current_position_tab,
            p.TAMAÑO_BLOQUE,
            'C')

        self.colision_timer.start()

    def process_key(self, key: str) -> None:
        """
        Procesa la key de movimiento y se valida el moviemiento
        """
        posicion_valida = validar_direccion(
            self.laberinto, self.current_position[::-1], key)

        if not self.paused:

            if not self.moving and posicion_valida:
                self.moving = True

                if key == 'W':
                    self.current_dir = -1
                    self.current_pixmap_key = 'C_U_1'
                    self.move('y')

                elif key == 'S':
                    self.current_dir = 1
                    self.current_pixmap_key = 'C_D_1'
                    self.move('y')

                elif key == 'A':
                    self.current_dir = -1
                    self.current_pixmap_key = 'C_L_1'
                    self.move('x')

                elif key == 'D':
                    self.current_dir = 1
                    self.current_pixmap_key = 'C_R_1'
                    self.move('x')

                self.last_key = key

    def move(self, axis: str) -> None:
        """
        Crea el timer de animacion de posicion
        """

        x = self.current_position[0]
        y = self.current_position[1]

        self.current_position_tab = [self.x_tab(x), self.y_tab(y)]

        self.timer = QTimer()
        # EXPLICACION DE ESE TIEMPO
        # p.VELOCIDAD_CONEJO = Vc = 10 [casilla/sec]
        # tiempo_conejo = tc = 1/Vc = 1/10 [sec/casilla]

        # luego debemos considerar el tamano de mi casilla
        # p.TAMAÑO_BLOQUE = Tb = 32 [pixeles/casilla]

        # entonces t_timer[sec] = tc x 1/Tb == (1/10 [sec/casilla]) x (1/32 [casilla/pixel])
        # se cancelan las casillas

        # luego el timer solo acepta en msec -> [1000 msec]/[1 sec]

        # t_timer[sec] == 1000/(10 x 32) [msec/pixel] = 1000/320 [msec/pixel]

        if self.frezzed:
            self.timer.setInterval(
                round(1000/(p.VELOCIDAD_CONEJO * p.TAMAÑO_BLOQUE * (1 - p.REDUCCION_VELOCIDAD))))
        else:
            self.timer.setInterval(
                round(1000/(p.VELOCIDAD_CONEJO * p.TAMAÑO_BLOQUE)))

        self.timer.timeout.connect(self.timer_methods[axis])

        self.active_timers['movement'] = self.timer

        self.timer.start()

    def animated_move_h(self) -> None:
        """
        Animacion de movimiento de una casilla a otra del tablero
        """
        if self.mapa.get(tuple(self.current_position), None) == 'EX':
            self.killed_by_ex()

        elif self.mapa.get(tuple(self.current_position), None) == 'CO':
            self.frezzed_by_ex()

        # calculamos la posicion en tablero de la sgte casilla, usando la posicion interna
        x_final = self.x_tab(self.current_position[0] + (1 * self.current_dir))

        if x_final < p.PADDING_MENU:
            self.moving = False
            self.timer.stop()
        # si no estamops en esa posicion
        if x_final != self.current_position_tab[0]:

            # nos movemos un pixel en la direccion indicada
            self.current_position_tab[0] += (1 * self.current_dir)

            # actualizamos nuestro pixmap
            self.current_pixmap_key = self.change_pixmap(self.current_dir, 'x')

            # lo emitimos al frontend
            self.senal_move.emit(
                self.current_position_tab,
                self.current_pixmap_key
            )

            # emitimos nuestra posicion al diccionario global
            self.senal_actualizar_pos.emit(self, self.current_position_tab)

        # llegamos a la posicion de la siguente casilla
        elif x_final == self.current_position_tab[0]:

            # actualizamos nuestra posicion interna
            self.current_position[0] += (1 * self.current_dir)
            # print(self.current_position)

            # si la posicion interna es igual al final cambiamos de nivel
            # y detenemos el timer
            if self.current_position == self.end_pos:
                self.senal_change_lvl.emit()

                self.moving = False
                self.timer.stop()

            # si un no se llega a la posicion final
            else:
                # calculamos la posicion siguente
                next_pos = (self.current_position[0] + (1 * self.current_dir),
                            self.current_position[1])

                # consultamos si es que nos podemos mover a esa posicion
                if self.mapa.get(next_pos, None) in self.walls:
                    # si es que no nos podemos mover, detenemos el timer
                    self.moving = False
                    self.timer.stop()

    def animated_move_v(self) -> None:
        """
        Funcionamiento analogo al anterior
        """
        # primero comprobamos que no hayamos muerto
        if self.mapa.get(tuple(self.current_position), None) == 'EX':
            self.killed_by_ex()

        elif self.mapa.get(tuple(self.current_position), None) == 'CO' and not self.frezzed:
            self.frezzed_by_ex()

        y_final = self.y_tab(self.current_position[1] + (1 * self.current_dir))

        if y_final < 0:
            self.moving = False
            self.timer.stop()

        if y_final != self.current_position_tab[1]:
            self.current_position_tab[1] += (1 * self.current_dir)

            self.current_pixmap_key = self.change_pixmap(self.current_dir, 'y')

            self.senal_move.emit(
                self.current_position_tab,
                self.current_pixmap_key
            )

            # emitimos nuestra posicion al diccionario global
            self.senal_actualizar_pos.emit(self, self.current_position_tab)

        elif y_final == self.current_position_tab[1]:

            # actualizar posicion
            self.current_position[1] += (1 * self.current_dir)
            # print(self.current_position)

            # if riesgo_mortal(self.laberinto, self.current_position[::-1]):
            #     # print('PELIGRO de COLISION')
            #     self.senal_risk_colision.emit(self)

            if self.current_position == self.end_pos:
                self.senal_change_lvl.emit()

                self.moving = False
                self.timer.stop()

            else:
                next_pos = (self.current_position[0],
                            self.current_position[1] + (1 * self.current_dir))

                if self.mapa.get(next_pos, None) in self.walls:
                    self.moving = False
                    self.timer.stop()

    def change_pixmap(self, current_dir: int, axis: str) -> str:
        """
        Si la posicion en tablero es multiplo de 32, cambiamos de pixmap en base a la direccion
        """
        i = next(self.generador)

        if axis == 'x' and self.current_position_tab[0] % p.PIXELS_CAMBIO_PIXMAP == 0:

            if current_dir == 1:  # derecha
                return f'C_R_{i}'

            elif current_dir == -1:  # izquierda
                return f'C_L_{i}'

            return self.current_pixmap_key

        elif axis == 'y' and self.current_position_tab[1] % p.PIXELS_CAMBIO_PIXMAP == 0:

            if current_dir == 1:  # abajo
                return f'C_D_{i}'

            elif current_dir == -1:  # arriba
                return f'C_U_{i}'

        return self.current_pixmap_key

    def pause(self) -> None:
        """
        Detiene el movimiento del conejo, luego se puede reanudar en la posicion actual
        """

        if self.paused:
            self.paused = False
            self.process_key(self.last_key)
        else:

            if self.active_timers.get('movement', None) is not None:
                self.active_timers['movement'].stop()
            self.moving = False
            self.paused = True

    def check_collision(self) -> None:
        if riesgo_mortal(self.laberinto, self.current_position[::-1]):
            # print('PELIGRO de COLISION')
            self.senal_risk_colision.emit(self)
            # print('peligrooo')

        elif self.mapa[tuple(self.current_position)] == 'EX':
            self.killed_by_ex()

    def killed_by_ex(self):
        if not self.killed:
            print('> Player killed by explotion')
            self.senal_killed_by_ex.emit()
            self.killed = True

    def frezzed_by_ex(self):
        if not self.frezzed:
            print('> Player frezzed by explotion')
            self.timer.setInterval(
                round(1000/(p.VELOCIDAD_CONEJO * p.TAMAÑO_BLOQUE * (1-p.REDUCCION_VELOCIDAD))))
            self.frezzed = True
