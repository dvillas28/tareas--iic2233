from PyQt6.QtCore import QObject
import backend.logica_utils.parametros as p
import json
from os.path import join


def validacion_formato(nombre: str) -> bool:
    """
    Un nombre es valido si: Es alfanumerico, tiene al menos una Mayus, y al menos un numero.
    Ademas 3 <= largo <= 16
    """
    alfanumerico: bool = nombre.isalnum()
    al_menos_una_mayus: bool = False
    al_menos_un_numero: bool = False

    for letra in nombre:
        if letra.isupper():
            al_menos_una_mayus = True

        elif letra.isdigit():
            al_menos_un_numero = True

    if alfanumerico and al_menos_una_mayus and al_menos_un_numero:
        if 3 <= len(nombre) <= 16:
            return True

    return False


def calcular_puntaje(tiempo: int, vidas: int, cantidad_lobos: int, PUNTAJE_LOBO: int) -> float:
    try:
        valor = round((tiempo * vidas) / (cantidad_lobos * PUNTAJE_LOBO), 2)

    except ZeroDivisionError:
        valor = 0.0

    return valor


def usar_item(item: str, inventario: list) -> tuple[bool, list]:
    """
    Si el item esta en el inventario, retorna una tupla con True y el inventario con el item
    removido, si no lo esta, retorna una tupla con False y el inventario sin modificar
    """

    if item not in inventario:
        return (False, inventario)

    # inventario.remove(item)
    return (True, inventario)


def load_laberinto(nivel: int) -> list:
    """
    Carga el archivo del laberinto en una lista de listas
    """

    laberinto = []
    with open(join(*(p.RUTA_TABLERO_BASE + f'{nivel}' + '.txt').split('/')), 'r') as file:
        # with open(join(*(p.RUTA_TABLERO_BASE + f'{4}' + '.txt').split('/')), 'r') as file:
        lineas = file.readlines()

    for linea in lineas:
        fila = linea.strip().split(',')
        if fila != ['']:
            laberinto.append(fila)

    return laberinto


def duracion_nivel() -> dict:

    ponderadores = {
        1: p.PONDERADOR_LABERINTO_1,
        2: p.PONDERADOR_LABERINTO_2,
        3: p.PONDERADOR_LABERINTO_3
    }

    d = {}

    current_tiempo = p.DURACION_NIVEL_INICIAL

    for i in range(1, 4):
        current_tiempo *= ponderadores[i]
        d[i] = current_tiempo

    return d


def velocidades_lobo() -> dict:
    ponderadores = {
        1: p.PONDERADOR_LABERINTO_1,
        2: p.PONDERADOR_LABERINTO_2,
        3: p.PONDERADOR_LABERINTO_3
    }

    d = {}

    current_spd = p.VELOCIDAD_LOBO

    for i in range(1, 4):
        current_spd = round(current_spd / ponderadores[i])
        d[i] = current_spd

    return d


def x_tab(x: int) -> int:
    """
    Retorna la representacion de x en el tablero
    """
    return x * p.TAMAÑO_BLOQUE + p.PADDING_MENU


def y_tab(y: int) -> int:
    """
    Retorna la representacion de y en el tablero
    """
    return y * p.TAMAÑO_BLOQUE


def x_untab(x_tab: int) -> int:
    """
    Realiza la operacion inversa
    """
    return (x_tab - p.PADDING_MENU) // p.TAMAÑO_BLOQUE


def y_untab(y_tab: int) -> int:
    """
    Realiza la operacion inversa
    """
    return y_tab // p.TAMAÑO_BLOQUE


def entities_overlapping(player: QObject, entity: QObject) -> bool:
    pos_1 = player.current_position_tab
    pos_2 = entity.current_position_tab

    # lados del jugador
    left_1 = pos_1[0]
    right_1 = pos_1[0] + p.ANCHO_LABERINTO

    top_1 = pos_1[1]
    bottom_1 = pos_1[1] + p.LARGO_LABERINTO

    # lados de la entidad
    left_2 = pos_2[0]
    right_2 = pos_2[0] + p.ANCHO_LABERINTO

    top_2 = pos_2[1]
    bottom_2 = pos_2[1] + p.LARGO_LABERINTO

    overlapping = (right_1 > left_2) and (right_2 > left_1) and (
        bottom_1 > top_2) and (bottom_2 > top_1)

    return overlapping


def get_columna(laberinto: list[list], columna: int) -> list:
    """
    Dado un laberinto y el numero de una columna. Retorna una lista unidimensional que representa a
    la columna.
    """
    lista = []

    # llegamos a la columna deseada
    for id_fila in range(len(laberinto)):
        for id_columna in range(len(laberinto[0])):
            # si la celda es parte de esa columna, la añadimos a la lista
            if id_columna == columna:
                celda = laberinto[id_fila][id_columna]
                lista.append(celda)

    return lista


def separate_list(list: list, separator: str):
    sublists = []
    actual_sublist = []

    for index, element in enumerate(list):
        if element == separator:
            if actual_sublist:
                sublists.append(actual_sublist)
            actual_sublist = []

        else:
            actual_sublist.append(index)

    if actual_sublist:
        sublists.append(actual_sublist)

    return sublists


# FUNCIONES MISCELANEAS QUE HACEN DE METODOS EN LA CLASE
def start_level_func(self, level) -> None:
    print(f'> Cargando Nivel {level}')
    self.senal_set_title.emit(self.user_name, level, self._vidas)
    self.create_map(level)
    self.create_lobos_entities(level)
    self.player.spawn()
    self.actualizar_posicion(self.player, self.player.current_position_tab)
    self.tiempo = round(self.duracion_niveles[self.curr_level])
    self.tiempo_actual = self.tiempo
    self.senal_cambio_segundos.emit(self.tiempo_actual)

    if not self.kil_shorcut_activated:
        self.start_all_entities()

    if not self.inf_shorcut_activated:
        self.duracion_timer.start()  # con tiempo_actual seteado


def pausar_func(self) -> None:
    if not self.game_paused:
        print('> Pausando Juego')
        self.game_paused = True
        self.duracion_timer.stop()

    else:
        print('> Resumiendo Juego')
        self.game_paused = False
        self.duracion_timer.start()

    self.player.pause()
    [lobo.pause() for lobo in self.lobos]
    [canon.pause() for canon in self.canones]
    [za.pause() for canon in self.canones for za in canon.bullets]


def limpiar_datos_func(self) -> None:
    [entity.active_timers['movement'].stop() for entity in self.lobos]
    self.lobos.clear()

    [zan.active_timers['movement'].stop()
     for canon in self.canones for zan in canon.bullets]

    self.canones.clear()
    self.posiciones_entidades.clear()
    self.senal_delete_entities.emit()


def process_key_func(self, key: str) -> None:
    """
    Funcion de procesado de teclas 
    """

    if key in ['W', 'A', 'S', 'D']:
        self.player.process_key(key)

    elif key == 'P':
        self.pausar()

    elif key == 'K':
        self.k_pressed = True

    elif key == 'I':
        self.i_pressed = True

    elif key == 'L' and self.i_pressed:  # K+I+L pressed
        kill_shorcut(self)
        self.k_pressed = False
        self.i_pressed = False

    elif key == 'N' and self.i_pressed:
        self.n_pressed = True

    elif key == 'F' and self.n_pressed:  # I+N+F pressed
        inf_shorcut(self)
        self.i_pressed = False
        self.n_pressed = False

    elif key == 'G':
        self.try_to_get_item()

    elif key == 'H':
        self.curr_item_selected = None
        print('> Seleccion de item cancelada')


def kill_shorcut(self) -> None:
    print(f'> K+I+L: Eliminando enemigos')
    self.kil_shorcut_activated = True
    self.limpiar_datos()


def inf_shorcut(self) -> None:
    print(f'> I+N+F: Tiempo detenido y vidas infinitas')
    self.inf_shorcut_activated = True
    self.inf_lives_sum = 1
    self.duracion_timer.stop()


def save_and_send(self, status: str):
    data = [status, self.user_name, self.curr_level, self.curr_points]
    print(
        f'> Enviando {self.user_name}, {self.curr_level}, {self.curr_points}')
    self.senal_enviar_data_al_server.emit(
        f'save;{json.dumps(data)}')


def game_over(self) -> None:
    print('> GAME OVER. Enviando datos al servidor')
    self.senal_send_music.emit('derrota')
    save_and_send(self, status='perdio en el')
    self.senal_juego_terminado_pop_up.emit(
        'Derrota :(', self.user_name, self.curr_level, self.curr_points)


def game_finished(self) -> None:
    print('> JUEGO COMPLETADO. Enviando datos al servidor')
    self.senal_send_music.emit('victoria')
    save_and_send(self, status='completo el')
    self.senal_juego_terminado_pop_up.emit(
        'Victoria! :)', self.user_name, self.curr_level, self.curr_points)
