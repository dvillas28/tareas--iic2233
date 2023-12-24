import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QFrame, QPushButton, QLabel, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtMultimedia import QSoundEffect
import frontend.parametros_frontend as p
from frontend.labels import MovableLabel, ImmovableLabel, ItemLabel
from frontend.pixmaps import load_pixmaps
from frontend.sounds import load_sounds


class VentanaJuego(QWidget):
    senal_salir_ventana_juego = pyqtSignal()
    senal_key_press = pyqtSignal(str)

    senal_pausar = pyqtSignal()
    senal_pos = pyqtSignal(int, int)
    # UNUSED
    senal_selected_item = pyqtSignal(int)
    senal_used_item = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.set_fixed_dimensions(p.DIMENSIONES_VENTANA_JUEGO +
                                  p.PADDING_MENU, p.DIMENSIONES_VENTANA_JUEGO)

        self.pixmaps = load_pixmaps()
        self.sounds = load_sounds()

        self.player = MovableLabel(
            tipo='Player', parent=self, pixmaps=self.pixmaps['conejo'])

        # set de movable labels
        self.entities = {}

        # inventraio
        self.inventory_labels = {}

        self.media_player_wav = QSoundEffect(self)

        self.font = self.set_font(p.FUENTE, size=p.TAMANO_FUENTE)
        self.create_menu()

    def set_fixed_dimensions(self, dim_x: int, dim_y) -> None:
        self.setGeometry(0, 0, dim_x, dim_y)
        self.setMaximumSize(dim_x, dim_y)
        self.setMinimumSize(dim_x, dim_y)

    def create_menu(self):

        self.menu_frame = QFrame(self)
        self.menu_frame.setGeometry(
            0, 0, p.PADDING_MENU, p.DIMENSIONES_VENTANA_JUEGO)
        self.menu_frame.setStyleSheet(f"background-color: rgb{p.LIGHT_PINK}")

        self.time_label = QLabel(self, text="Tiempo: 120 segundos")
        self.time_label.setFont(self.font)
        self.time_label.move(20, 20)
        self.time_label.resize(self.time_label.sizeHint())

        self.lives_label = QLabel(self, text="Vidas restantes: 3")
        self.lives_label.setFont(self.font)
        self.lives_label.move(20, 50)
        self.lives_label.resize(self.lives_label.sizeHint())

        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.setStyleSheet(f"background-color: rgb{p.DARK_PINK}")
        self.boton_salir.setFont(self.font)
        self.boton_salir.move(10, 100)
        self.boton_salir.resize(self.boton_salir.sizeHint())
        self.boton_salir.clicked.connect(self.salir)

        self.boton_pausa = QPushButton("Pausa", self)
        self.boton_pausa.setStyleSheet(f"background-color: rgb{p.DARK_PINK}")
        self.boton_pausa.setFont(self.font)
        self.boton_pausa.move(105, 100)
        self.boton_pausa.resize(self.boton_pausa.sizeHint())
        self.boton_pausa.clicked.connect(self.pausar)

        self.item_frame = QFrame(self)
        self.item_frame.move(20, 145)
        self.item_frame.resize(160, 350)
        self.item_frame.setStyleSheet(
            f"background-color: rgb{p.INVENTORY_PINK}")

        self.inventario_label = QLabel(self, text="Inventario")
        self.inventario_label.setFont(self.font)
        self.inventario_label.move(60, 150)

        # el maximo de objetos que el usuario puede recoger, basado en mi implementacion
        # (donde el inventario se pierde al perder una vida) es 5
        self.item1 = ItemLabel(
            self.item_frame, self.senal_selected_item, self.pixmaps['items'])
        self.item1.setGeometry(15, 30, 33, 33)
        self.inventory_labels[1] = self.item1

        self.item2 = ItemLabel(
            self.item_frame, self.senal_selected_item, self.pixmaps['items'])
        self.item2.setGeometry(63, 30, 33, 33)
        self.inventory_labels[2] = self.item2

        self.item3 = ItemLabel(
            self.item_frame, self.senal_selected_item, self.pixmaps['items'])
        self.item3.setGeometry(111, 30, 33, 33)
        self.inventory_labels[3] = self.item3

        self.item4 = ItemLabel(
            self.item_frame, self.senal_selected_item, self.pixmaps['items'])
        self.item4.setGeometry(15, 78, 33, 33)
        self.inventory_labels[4] = self.item4

        self.item5 = ItemLabel(
            self.item_frame, self.senal_selected_item, self.pixmaps['items'])
        self.item5.setGeometry(63, 78, 33, 33)
        self.inventory_labels[5] = self.item5

        self.item6 = ItemLabel(
            self.item_frame, self.senal_selected_item, self.pixmaps['items'])
        self.item6.setGeometry(111, 78, 33, 33)
        self.inventory_labels[6] = self.item6

        self.item7 = ItemLabel(
            self.item_frame, self.senal_selected_item, self.pixmaps['items'])
        self.item7.setGeometry(15, 126, 33, 33)
        self.inventory_labels[7] = self.item7

        self.item8 = ItemLabel(
            self.item_frame, self.senal_selected_item, self.pixmaps['items'])
        self.item8.setGeometry(63, 126, 33, 33)
        self.inventory_labels[8] = self.item8

        self.item9 = ItemLabel(
            self.item_frame, self.senal_selected_item, self.pixmaps['items'])
        self.item9.setGeometry(111, 126, 33, 33)
        self.inventory_labels[9] = self.item9

        # labels de resultados finales
        self.frame_de_resultados = self.results_frame()

    def place_item_inventory(self, tipo, ide):
        self.inventory_labels[ide].tipo = tipo
        self.inventory_labels[ide].place_pixmap(tipo)

    def item_usado(self, ide: int) -> None:
        self.inventory_labels[ide].reset_item()

    def set_font(self, font_: str, size: int = 10) -> QFont:
        font = QFont()
        font.setPointSize(size)
        font.setFamily(font_)

        return font

    def set_title(self, name: str, level: int, vidas: int) -> None:
        self.setWindowTitle(f'{name} - nivel {level}')
        self.lives_label.setText(f"Vidas restantes: {vidas}")
        self.lives_label.resize(self.lives_label.sizeHint())

    def cambiar_segundos(self, sec: int):
        self.time_label.setText(f"Tiempo: {sec} segundos")
        self.time_label.resize(self.time_label.sizeHint())

    def results_frame(self) -> QFrame:
        self.frame_final = QFrame(self)
        self.frame_final.setGeometry(200, 150, 512, 200)
        self.frame_final.setStyleSheet(f"background-color: rgb{p.DARK_PINK}")

        self.boton_salir_juego = QPushButton("Salir", self.frame_final)
        self.boton_salir_juego.setStyleSheet(
            f"background-color: rgb{p.LIGHT_PINK}")
        self.boton_salir_juego.setFont(self.font)
        self.boton_salir_juego.move(215, 150)
        self.boton_salir_juego.resize(self.boton_salir_juego.sizeHint())
        self.boton_salir_juego.clicked.connect(self.salir)

        # labels de informacion
        self.result_label = QLabel(self.frame_final, text='<status>')
        self.result_label.move(187, 20)
        self.result_label.setFont(self.font)

        # label con el nombre de usuario
        self.user_name_label = QLabel(self.frame_final, text='Usuario:')
        self.user_name_label.move(167, 60)
        self.user_name_label.setFont(self.font)
        # label con el puntaje
        self.puntaje_label = QLabel(
            self.frame_final, text=f'Puntaje total: ')

        self.puntaje_label.move(167, 100)
        self.puntaje_label.setFont(self.font)

        return self.frame_final

    def juego_terminado(self, msg: str, username: str, level: str, puntos: str):
        # setear las variables que llegaron
        self.result_label.setText(msg)
        self.result_label.resize(self.result_label.sizeHint())

        self.user_name_label.setText(f'Usuario: {username}')
        self.user_name_label.resize(self.user_name_label.sizeHint())

        self.puntaje_label.setText(f'Puntaje Total: {puntos}')
        self.puntaje_label.resize(self.puntaje_label.sizeHint())

        self.frame_de_resultados.raise_()
        self.frame_de_resultados.show()

    def salir(self, error: bool) -> None:
        # modo de salir en caso de que haya habido una desconexion del server
        if error:
            err = QMessageBox.critical(
                self, 'Error', "Desconexion repentina del servidor")

        QApplication.quit()

    def closeEvent(self, event) -> None:
        # metodo en caso de que se cierre con la X
        # cerrar con el boton redirige a este metodo igual
        self.senal_salir_ventana_juego.emit()
        QApplication.quit()
        event.accept()

    def pausar(self):
        self.senal_pausar.emit()

    def play_sound(self, sound_key) -> None:
        file_url = self.sounds[sound_key]
        self.media_player_wav.setSource(file_url)
        self.media_player_wav.play()

    def mostrar_popup(self, msg: str) -> None:
        alert = QMessageBox.information(self, '', msg)

    # metodos miscelaneos
    def start_simulation(self) -> None:
        self.show()

    def keyPressEvent(self, event):
        try:
            self.senal_key_press.emit(chr(event.key()))

        except ValueError:
            pass

    def place_tile(self, x: int, y: int, size: int,
                   primary_key: str, secondary_key: str, tipo: str) -> None:
        # senal llamada por el backend para colocar un bloque
        block = ImmovableLabel(tipo, self.senal_pos, self)
        block.move(x, y)
        block.resize(size, size)

        block_pixmap = self.pixmaps[primary_key][secondary_key]

        block.setPixmap(block_pixmap)
        block.setScaledContents(True)
        block.show()

    def create_movable_label(self, tipo, ide: int, primary_key: str) -> None:
        # metodo llamado por senal_create_entity_object
        label = MovableLabel(tipo=tipo, parent=self,
                             pixmaps=self.pixmaps[primary_key])

        self.entities[f'{tipo}{ide}'] = label
        # print(f'Creado label {tipo}{ide}')

    def delete_current_labels(self) -> None:
        # metodo llamado por senal_delete_entities
        [entity.clear() for entity in list(self.entities.values())]
        self.entities.clear()
        # print('Diccionario de entidades limpio')

    def spawn_entity(self, pos: list, size: int, pix_key: str, tipo: str, ide: int):
        # metodo llamado por senal para buscar al objeto que
        # queremos iniciar actualmente
        self.entities[f'{tipo}{ide}'].spawn_label(pos, size, pix_key)

    def move_entity(self, pos: list, pix_key: str, tipo: str, ide: int):
        self.entities[f'{tipo}{ide}'].move_label(pos, pix_key)

    def kill_entity(self, tipo: str, ide: int):
        self.entities[f'{tipo}{ide}'].clear()
        self.entities.pop(f'{tipo}{ide}')


if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)

    sys.__excepthook__ = hook
    app = QApplication([])
    ventana = VentanaJuego()
    ventana.show()
    sys.exit(app.exec())
