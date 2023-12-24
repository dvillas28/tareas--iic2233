from time import sleep
from PyQt6.QtCore import QThread, pyqtSignal
from backend.logica_utils.funciones_logica import x_tab, y_tab, separate_list, get_columna
from backend.logica_utils import parametros as p


class Item(QThread):
    identificador = 1

    def __init__(self, senal_place: pyqtSignal,
                 senal_deactivate: pyqtSignal, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.identificador = Item.identificador
        Item.identificador += 1
        self.senal_place = senal_place
        self.senal_deactivate = senal_deactivate

        self.effect: str = None
        self.curr_map: dict = None
        self.curr_laberinto: list = None
        self.x: int = None
        self.y: int = None

        self.player_killed = False

    def get_affected_tiles(self, laberinto: list, x: int, y: int):
        # tenemos la lista de lista
        # nos colocamos en la posicion dada por x: columna, y: fila

        # analisis vertical
        column = get_columna(laberinto, x)
        affected_column: list = []

        # dividimos la sublista en sus indices
        sub_columns = separate_list(column, 'P')
        for sub_column in sub_columns:
            if y in sub_column:
                for id_y in sub_column:
                    affected_column.append((x, id_y))
                break

        # analisis horizontal
        row = laberinto[y]
        affected_row: list = []

        # dividimos la sublista en sus indices
        sub_rows = separate_list(row, 'P')
        for sub_row in sub_rows:
            if x in sub_row:
                for id_x in sub_row:
                    affected_row.append((id_x, y))
                break

        return affected_column + affected_row

    def act(self, name: str) -> None:
        print(f'> Item {name} actuando!')

    def run(self):
        affected_tiles = self.get_affected_tiles(
            self.curr_laberinto, self.x, self.y)

        for aff_tuple in affected_tiles:
            x, y = aff_tuple[0], aff_tuple[1]

            if self.effect == 'EX':
                self.senal_place.emit(x_tab(x), y_tab(
                    y), p.TAMAÑO_BLOQUE, 'items', self.effect, 'item')

                # actualizamos el mapa
                self.curr_map[(x, y)] = self.effect

            elif self.effect == 'CO':

                if self.curr_map[(x, y)] not in ['CD', 'CU', 'CL', 'CR']:
                    self.senal_place.emit(x_tab(x), y_tab(y),
                                          p.TAMAÑO_BLOQUE, 'items', self.effect, 'item')

                    # actualizamos el mapa
                    self.curr_map[(x, y)] = self.effect

        sleep(p.TIEMPO_BOMBA)

        if not self.player_killed:

            for aff_tuple in affected_tiles:
                x, y = aff_tuple[0], aff_tuple[1]
                if self.effect == 'EX':

                    self.senal_place.emit(x_tab(x), y_tab(y),
                                          p.TAMAÑO_BLOQUE, 'tiles', '-', 'suelo')

                    self.curr_map[(x, y)] = '-'

                elif self.effect == 'CO':
                    if self.curr_map[(x, y)] not in ['CD', 'CU', 'CL', 'CR']:
                        self.senal_place.emit(x_tab(x), y_tab(y),
                                              p.TAMAÑO_BLOQUE, 'tiles', '-', 'suelo')

                    self.curr_map[(x, y)] = '-'

            self.senal_deactivate.emit(self.identificador)


class Manzana(Item):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo: str = 'M'
        self.name: str = 'Manzana'
        self.effect: str = 'EX'

    def set_effect(self, mapa: dict, laberinto: list, x: int, y: int):
        super().act(self.name)
        self.curr_map = mapa
        self.curr_laberinto = laberinto

        self.x = x
        self.y = y


class Congelador(Item):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tipo: str = 'CO'
        self.name: str = 'Congelador'
        self.effect: str = 'CO'

    def set_effect(self, mapa: dict, laberinto: list, x: int, y: int):
        super().act(self.name)
        self.curr_map = mapa
        self.curr_laberinto = laberinto

        self.x = x
        self.y = y
