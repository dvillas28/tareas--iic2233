from PyQt6.QtCore import QObject, pyqtSignal, QTimer
from backend.logica_utils.funciones_logica import (duracion_nivel,
                                                   velocidades_lobo,
                                                   calcular_puntaje, load_laberinto,
                                                   x_tab, y_tab, x_untab, y_untab,
                                                   entities_overlapping,
                                                   start_level_func,
                                                   pausar_func,
                                                   limpiar_datos_func,
                                                   process_key_func, save_and_send,
                                                   game_over, game_finished, usar_item)
from backend.logica_utils import parametros as p
from backend.logica_utils.player import Player
from backend.logica_utils.lobo import Lobo
from backend.logica_utils.canon import Canon
from backend.logica_utils.zanahoria import Zanahoria
from backend.logica_utils.item import Item, Manzana, Congelador


class LogicaJuego(QObject):
    senal_start_simulation = pyqtSignal()
    senal_cerrar_ventana_por_desconexion = pyqtSignal(bool)
    senal_on_front_close = pyqtSignal()
    senal_enviar_data_al_server = pyqtSignal(str)
    senal_set_title = pyqtSignal(str, int, int)
    senal_cambio_segundos = pyqtSignal(int)
    senal_place_tile = pyqtSignal(int, int, int, str, str, str)
    senal_spawn_player = pyqtSignal(list, int, str)
    senal_move_player = pyqtSignal(list, str)
    senal_colision_risk = pyqtSignal(QObject)
    senal_raise_player_label = pyqtSignal()
    senal_actualizar_posicion = pyqtSignal(QObject, list)
    senal_change_lvl = pyqtSignal()
    senal_create_entity_label = pyqtSignal(str, int, str)
    senal_delete_entities = pyqtSignal()
    senal_spawn_entity = pyqtSignal(list, int, str, str, int)
    senal_move_entity = pyqtSignal(list, str, str, int)
    senal_kill_entity = pyqtSignal(QObject)
    senal_kill_entity_label = pyqtSignal(str, int)
    senal_send_music = pyqtSignal(str)
    senal_mensaje_pop_up = pyqtSignal(str)
    senal_juego_terminado_pop_up = pyqtSignal(str, str, int, float)
    senal_place_item_inventory = pyqtSignal(str, int)
    senal_deactivate_item = pyqtSignal(int)
    senal_deactivate_item_label = pyqtSignal(int)
    senal_player_killed_by_ex = pyqtSignal()
    senal_lobo_frezzed = pyqtSignal(int)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.map = {}
        self.player = Player('conejo', self.senal_spawn_player,
                             self.senal_move_player, self.senal_change_lvl,
                             self.senal_actualizar_posicion, self.senal_colision_risk,
                             self.senal_player_killed_by_ex)

        self.conectar_senales_internas()

        self.user_name: str = None
        self.curr_level: int = None
        self.curr_points: int = None

        self.lobos: list = []
        self.lobos_eliminados: list = []
        self.lobos_frezzed: list = []

        self.canones: list = []

        self.posiciones_entidades = {}

        self.velocidades_lobo = velocidades_lobo()
        self.duracion_niveles = duracion_nivel()

        self.duracion_timer = QTimer()
        self.duracion_timer.setInterval(1000)  # cada 1 sec
        self.duracion_timer.timeout.connect(self.cambiar_segundos)

        self.game_paused: bool = False

        self.inf_shorcut_activated: bool = False
        self.inf_lives_sum = 0

        self.kil_shorcut_activated: bool = False

        self.items_classes = {'BC': Congelador, 'BM': Manzana}
        self.inventario = {}
        self.curr_item_selected: Item = None

    def conectar_senales_internas(self) -> None:
        self.senal_change_lvl.connect(self.next_level)
        self.senal_actualizar_posicion.connect(self.actualizar_posicion)
        self.senal_colision_risk.connect(self.handle_colision)
        self.senal_kill_entity.connect(self.kill_entity)
        self.senal_deactivate_item.connect(self.deactivate_item)
        self.senal_player_killed_by_ex.connect(self.player_hit)
        self.senal_lobo_frezzed.connect(self.add_frezzed_lobo)

    def salir_ventana_juego(self) -> None:
        print(f"> Backend_J: Frontend Cerrado: Avisando a cliente")
        self.senal_on_front_close.emit()

    def cerrar_ventana_por_desconexion(self) -> None:
        self.senal_cerrar_ventana_por_desconexion.emit(True)

    def send_game_data(self, puntaje: int) -> None:
        print(
            f'> {self.user_name} completo el nivel {self.curr_level} con {puntaje} puntos')

    def load_game_data(self, user_name: str, level: int, points: float) -> None:
        self.user_name = user_name
        self.curr_level = int(level)
        self.curr_points = float(points)

        self._vidas = max(1, p.CANTIDAD_VIDAS - self.curr_level + 1)

    def start_simulation(self) -> None:
        self.senal_start_simulation.emit()
        self.start_level(self.curr_level)

    def start_level(self, level: int) -> None:
        start_level_func(self, level)

    def create_map(self, nivel: int) -> None:
        laberinto = load_laberinto(nivel)
        self.player.laberinto = laberinto

        for id_fila in range(p.ANCHO_LABERINTO):
            for id_columna in range(p.LARGO_LABERINTO):
                tipo = laberinto[id_fila][id_columna]
                x, y = x_tab(id_columna), y_tab(id_fila)

                if tipo in ["C", "LH", "LV", "S", "E", "-"]:
                    if tipo == 'E':
                        self.player.start_pos = [id_columna, id_fila]

                    elif tipo == 'S':
                        self.player.end_pos = [id_columna, id_fila]

                    self.map[(id_columna, id_fila)] = '-'
                    self.senal_place_tile.emit(
                        x, y, p.TAMAÑO_BLOQUE, 'tiles', '-', 'suelo')
                else:
                    if tipo != 'P':  # entonces en un cañon
                        self.senal_place_tile.emit(
                            x, y, p.TAMAÑO_BLOQUE, 'tiles', '-', 'suelo')

                    self.map[(id_columna, id_fila)] = tipo

                    if tipo == 'P':
                        self.senal_place_tile.emit(
                            x, y, p.TAMAÑO_BLOQUE, 'tiles', 'P', 'pared')

                    elif tipo in ['CU', 'CD', 'CL', 'CR']:
                        canon = Canon('zanahoria', tipo[1], [id_columna, id_fila],
                                      self.senal_create_entity_label, self.senal_spawn_entity,
                                      self.senal_move_entity, self.senal_kill_entity,
                                      self.senal_actualizar_posicion)

                        self.canones.append(canon)
                        self.senal_place_tile.emit(
                            x, y, p.TAMAÑO_BLOQUE, 'canon', tipo, 'cañon')

                    elif tipo == 'BM':
                        self.senal_place_tile.emit(
                            x, y, p.TAMAÑO_BLOQUE, 'items', 'BM', 'manzana')

                    elif tipo == 'BC':
                        self.senal_place_tile.emit(
                            x, y, p.TAMAÑO_BLOQUE, 'items', 'BC', 'congelacion')

        self.player.mapa = self.map  # le entregamos el mapa al jugador

    def create_lobos_entities(self, nivel: int):
        laberinto = load_laberinto(nivel)

        for id_fila in range(p.ANCHO_LABERINTO):
            for id_columna in range(p.LARGO_LABERINTO):
                tipo = laberinto[id_fila][id_columna]

                if tipo == 'LH':

                    lobo = Lobo('lobo_h', 'H', (id_columna, id_fila),
                                self.velocidades_lobo[self.curr_level],
                                self.senal_spawn_entity, self.senal_move_entity,
                                self.senal_actualizar_posicion, self.senal_kill_entity,
                                self.senal_lobo_frezzed)
                    self.lobos.append(lobo)

                elif tipo == 'LV':

                    lobo = Lobo('lobo_v', 'V', (id_columna, id_fila),
                                self.velocidades_lobo[self.curr_level],
                                self.senal_spawn_entity, self.senal_move_entity,
                                self.senal_actualizar_posicion, self.senal_kill_entity,
                                self.senal_lobo_frezzed)
                    self.lobos.append(lobo)

        for entity in self.lobos:
            self.senal_create_entity_label.emit(
                f'{entity.tipo}', entity.identificador, entity.primary_key)

    def start_all_entities(self):
        for entity in self.lobos:
            entity.mapa = self.map
            self.actualizar_posicion(entity, entity.current_position_tab)
            if entity.identificador in self.lobos_frezzed:
                entity.status = 'frezzed'

            entity.spawn()
            entity.move()

        for canon in self.canones:
            canon.mapa = self.map
            canon.start_timer()

    def kill_entity(self, entity: QObject) -> None:

        if isinstance(entity, Lobo) and entity.identificador not in self.lobos_eliminados:
            print('Lobo eliminado')
            self.lobos_eliminados.append(entity.identificador)

        if isinstance(entity, Canon):
            # parar su timer
            entity.shooting_timer.stop()

        else:
            self.posiciones_entidades.pop(entity)  # para evitar la colision
            self.senal_kill_entity_label.emit(
                entity.tipo, entity.identificador)

    def procesar_key_press(self, key: str) -> None:
        try:
            process_key_func(self, key)
        except AttributeError:
            pass  # si se presiona mal una tecla, no queremos que pase nada

    def pausar(self) -> None:
        pausar_func(self)

    # los lobos eliminados se deberia reiniciar solo al cambiar de nivel
    def next_level(self) -> None:
        if not self.inf_shorcut_activated:
            a1 = '> Calculando puntaje, numero de lobos eliminados'
            a2 = f'{self.curr_level}: {len(self.lobos_eliminados)}'
            print(a1 + a2)
            puntaje = calcular_puntaje(self.tiempo_actual, self._vidas,
                                       len(self.lobos_eliminados), p.PUNTAJE_LOBO)
            # puntaje = calcular_puntaje(17, 2, 0, 3)
        else:
            puntaje = p.PUNTAJE_INF

        self.curr_points += puntaje
        print(f'> Puntaje Actual: {self.curr_points}')
        self.curr_points = self.curr_points
        self.curr_level += 1

        if self.curr_level == 4:
            self.curr_level = 3
            game_finished(self)
            if not self.kil_shorcut_activated:
                self.limpiar_datos()
        else:
            save_and_send(self, status='paso al')
            if not self.kil_shorcut_activated:
                self.limpiar_datos()
            self.player.frezzed = False
            self.lobos_eliminados.clear()
            self.lobos_frezzed.clear()
            self.senal_start_simulation.emit()
            self.start_level(self.curr_level)
            print(f'> Usuario paso al nivel {self.curr_level}')

    def limpiar_datos(self) -> None:
        limpiar_datos_func(self)
        Lobo.identificador = 0
        Zanahoria.identificador = 0

    def clean_inventario(self) -> None:
        for key, value in self.inventario.items():
            value.player_killed = True
            self.deactivate_item(key)

            self.senal_deactivate_item_label.emit(
                key)  # se simula su uso para eliminarlo

        self.inventario.clear()

    def actualizar_posicion(self, entidad: QObject, posicion: list) -> None:
        self.posiciones_entidades[entidad] = posicion

    def handle_colision(self, player: QObject) -> bool:
        for key, pos in self.posiciones_entidades.items():
            if key != player:  # descartamos al jugador
                if entities_overlapping(player, key):
                    self.player_hit()
                    break
        return False

    def cambiar_segundos(self) -> None:
        self.tiempo_actual -= 1

        if self.tiempo_actual < 0:
            self.player_hit()
        else:
            self.senal_cambio_segundos.emit(self.tiempo_actual)

    def player_hit(self) -> None:
        self.player.active_timers['movement'].stop()
        self.player.moving = False
        self.player.paused = True

        self._vidas += (-1 + self.inf_lives_sum)
        if self._vidas == 0:
            game_over(self)
            self.limpiar_datos()
        elif self._vidas > 0:
            self.senal_start_simulation.emit()
            self.limpiar_datos()
            self.clean_inventario()  # se limpia solo si perdemos vidas
            self.start_level(self.curr_level)

    def procesar_posicion_clickeada(self, x: int, y: int) -> None:
        # metodo llamado por señal
        x, y = x_untab(x), y_untab(y)  # transformar a coordenadas internas
        self.use_item_selected(x, y)

    def procesar_item_seleccionado(self, ide: int) -> None:
        # metodo llamado por señal
        self.curr_item_selected = self.inventario[ide]
        print(f'Seleccionada: {self.inventario[ide].name}')

    def try_to_get_item(self) -> None:
        x, y = self.player.current_position[0], self.player.current_position[1]

        if self.map[(x, y)] in ['BC', 'BM']:
            item = self.items_classes[self.map[(x, y)]](
                self.senal_place_tile, self.senal_deactivate_item, )
            self.inventario[item.identificador] = item

            print(f'> Item {item.name} obtenido!')

            self.senal_place_tile.emit(x_tab(x), y_tab(
                y), p.TAMAÑO_BLOQUE, 'tiles', '-', 'suelo')
            self.map[(x, y)] = '-'

            self.senal_raise_player_label.emit()
            # emitir una senal para colocarlo en el inventario grafico
            self.senal_place_item_inventory.emit(item.tipo, item.identificador)
        else:
            print('> No item en esta posicion')

    def use_item_selected(self, x, y) -> None:
        if self.curr_item_selected is not None:
            if not self.game_paused:

                if usar_item(self.curr_item_selected, list(self.inventario.values())):

                    if self.map[(x, y)] == 'P' or self.map[(x, y)].startswith('C'):
                        print('> No puedes colocar un item ahi')
                        self.senal_mensaje_pop_up.emit(
                            'No puedes colocar un item ahi')

                    else:
                        # si es que hay un item seleccionado, ejecutar la accion de ese item
                        self.apply_item_effect(x, y)
            else:
                print('> Juego pausado')
        else:
            print('> No tienes un item seleccionado')

    def apply_item_effect(self, x: int, y: int) -> None:
        laberinto = load_laberinto(self.curr_level)
        self.senal_deactivate_item_label.emit(
            self.curr_item_selected.identificador)

        # hacemos actuar al item
        self.item = self.curr_item_selected

        self.item.set_effect(self.map, laberinto, x, y)
        self.item.start()

        # el thread deberia encargarse de actualizar el diccionario de posiciones

    def deactivate_item(self, ide: int) -> None:
        # y eliminarlo de los registros, pero sus efectos de mantienen por el nivel
        self.senal_raise_player_label.emit()
        # self.inventario.pop(ide)
        self.curr_item_selected = None

    def add_frezzed_lobo(self, ide: int) -> None:
        self.lobos_frezzed.append(ide)
