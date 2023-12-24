import sys
import os
from PyQt6.QtWidgets import (QApplication,
                             QWidget,
                             QPushButton,
                             QLineEdit,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                             QMessageBox)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import pyqtSignal, Qt
from frontend import parametros_frontend as p


class VentanaInicio(QWidget):
    # señal de de nombre valido hacia el backend
    senal_validar_nombre = pyqtSignal(str)
    senal_salir_ventana_inicio = pyqtSignal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(f"background-color: rgb{p.LIGHT_PINK}")
        self.set_fixed_dimensions(p.DIMENSIONES_VENTANA_INICIO)
        self.font = self.set_font(p.FUENTE, size=p.TAMANO_FUENTE)

        self.main_layout = QVBoxLayout()

        # Logo de DCConejo
        self.create_logo()

        # Label de Texto debajo del logo
        self.set_subtitle(text="¿Una partida?")

        # Linea de Texto para ingresar el nombre de usuario
        self.set_input_line(placeholder="Ingresa tu usuario")

        # Botones Para Comenzar la partida Y salir
        self.set_buttons()

        # salon fama
        self.label_jugadores = dict()
        self.set_salon_fama()

        # añadir todos los layouts
        self.set_layouts()

    def set_fixed_dimensions(self, dim: int) -> None:
        self.setGeometry(0, 0, dim, dim)
        self.setMaximumSize(dim, dim)
        self.setMinimumSize(dim, dim)

    def set_font(self, font_: str, size: int = 10) -> QFont:
        font = QFont()
        font.setPointSize(size)
        font.setFamily(font_)
        return font

    def create_logo(self) -> None:
        self.layout_logo = QVBoxLayout()
        self.label_logo = QLabel(self)
        self.label_logo.setGeometry(50, 40, 410, 70)

        path = os.path.join(*(p.RUTA_LOGO.split("/")))
        pixmap = QPixmap(path)

        self.label_logo.setPixmap(pixmap)
        self.label_logo.setScaledContents(True)

        self.layout_logo.addWidget(self.label_logo)

    def set_subtitle(self, text: str) -> None:
        self.layout_subtitulo = QHBoxLayout()
        self.label_subtitulo = QLabel(self, text=text)
        self.label_subtitulo.setFont(self.font)
        self.label_subtitulo.resize(self.label_subtitulo.sizeHint())
        self.layout_subtitulo.addStretch(1)
        self.layout_subtitulo.addWidget(self.label_subtitulo)
        self.layout_subtitulo.addStretch(1)

    def set_input_line(self, placeholder: str = "") -> None:
        self.layout_linea_texto = QHBoxLayout()
        self.linea_texto = QLineEdit(self)
        input_font = self.set_font("Ubuntu")
        self.linea_texto.setFont(input_font)
        self.linea_texto.setPlaceholderText(placeholder)
        self.linea_texto.resize(20, 80)
        self.layout_linea_texto.addWidget(self.linea_texto)

    def set_buttons(self) -> None:
        self.layout_botones = QHBoxLayout()
        self.boton_ingresar = QPushButton("Ingresar", self)
        self.boton_ingresar.setStyleSheet(
            f"background-color: rgb{p.DARK_PINK}")
        self.boton_ingresar.setFont(self.font)
        self.boton_ingresar.clicked.connect(self.try_to_enter)

        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.setStyleSheet(f"background-color: rgb{p.DARK_PINK}")
        self.boton_salir.setFont(self.font)
        self.boton_salir.clicked.connect(self.salir)

        self.layout_botones.addStretch(1)
        self.layout_botones.addWidget(self.boton_ingresar)
        self.layout_botones.addStretch(1)
        self.layout_botones.addWidget(self.boton_salir)
        self.layout_botones.addStretch(1)

    def try_to_enter(self) -> None:
        name = self.linea_texto.text()
        print(f"> V_Inicio: Tratando de entrar con {name}")
        self.senal_validar_nombre.emit(name)

    def salir(self, error: bool) -> None:
        # metodo llamado en caso de presionar el boton salir
        # o en caso de haber una desconexion del servidor
        if error:
            err = QMessageBox.critical(
                self, 'Error', "Desconexion repentina del servidor")
        QApplication.quit()

    def closeEvent(self, event) -> None:
        # metodo llamado en caso de presionar la X en la esquina
        # por alguna razon, este metodo tambien se llama al hacer el llamado
        # del metodo salir de arriba

        self.senal_salir_ventana_inicio.emit()
        QApplication.quit()
        event.accept()

    def ocultar_inicio(self) -> None:
        # metodo llamado por logica para cerrar esta ventana e iniciar la otra
        self.hide()

    def set_salon_fama(self) -> None:
        self.layout_puntajes = QHBoxLayout()
        self.layout_lista = QVBoxLayout()

        self.titulo = QLabel(self, text="Salón de la fama")
        self.titulo.setFont(self.font)

        self.p1 = QLabel(self, text='')
        self.p2 = QLabel(self, text='')
        self.p3 = QLabel(self, text='')
        self.p4 = QLabel(self, text='')
        self.p5 = QLabel(self, text='')

        self.p1.show()
        self.p2.show()
        self.p3.show()
        self.p4.show()
        self.p5.show()

        # los almacenamos en un diccionario
        self.label_jugadores[1] = self.p1
        self.label_jugadores[2] = self.p2
        self.label_jugadores[3] = self.p3
        self.label_jugadores[4] = self.p4
        self.label_jugadores[5] = self.p5

        # añadidos al widget
        self.layout_lista.addWidget(self.titulo)
        self.layout_lista.addWidget(self.p1)
        self.layout_lista.addWidget(self.p2)
        self.layout_lista.addWidget(self.p3)
        self.layout_lista.addWidget(self.p4)
        self.layout_lista.addWidget(self.p5)

        self.layout_puntajes.addStretch(1)
        self.layout_puntajes.addLayout(self.layout_lista)
        self.layout_puntajes.addStretch(1)

    def set_layouts(self) -> None:
        self.main_layout.addLayout(self.layout_logo)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout_subtitulo)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout_linea_texto)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout_botones)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(self.layout_puntajes)
        self.main_layout.addStretch(1)
        self.setLayout(self.main_layout)

    def iniciar_ventana_inicio(self) -> None:
        # metodo conectado a una señal del backend
        self.show()

    def anadir_jugador_data(self, jugador: str, puntaje: str, lugar: int) -> None:
        # metodo conectado a una señal del backend
        # print('> Ventana_de_inicio: dato de top 5, colocando ')
        self.label_jugadores[lugar].setText(
            f"{lugar}. {jugador}: {puntaje} puntos")

        self.label_jugadores[lugar].resize(
            self.label_jugadores[lugar].sizeHint())
        self.label_jugadores[lugar].show()

    def mostrar_popup(self, err_msg: str) -> None:
        alert = QMessageBox.critical(self, 'Error', err_msg)

        self.linea_texto.setText('')
        self.linea_texto.setFocus()


if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(value)
        print(traceback)

    sys.__excepthook__ = hook
    app = QApplication([])
    ventana = VentanaInicio()
    ventana.show()
    ventana.anadir_jugador('daniel', 10000, 1)
    ventana.anadir_jugador('daniel', 1000, 2)
    ventana.anadir_jugador('daniel', 100, 3)
    ventana.anadir_jugador('daniel', 10, 4)
    ventana.anadir_jugador('daniel', 1, 5)

    sys.exit(app.exec())
