from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtCore import Qt, pyqtSignal


class MovableLabel(QLabel):
    """
    Entidad grafica del conejo/lobo/zanahorias
    solo puede recolocarlo y cambiarle el pixmap, pero de cuando y como se encarga el backend
    """

    # debe poseer una senal para avisar q murio?
    # es posible

    def __init__(self, tipo: str, parent: QWidget, pixmaps: dict, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.tipo = tipo
        self.pixmaps = pixmaps

    def spawn_label(self, pos: list, size: int, default_pix_key: str) -> None:
        self.raise_()  # para que quede encima de las tiles
        self.move(*pos)
        self.resize(size, size)

        default = self.pixmaps[default_pix_key]
        self.setPixmap(default)  # seteamos el pixmap por defecto
        self.setScaledContents(True)
        self.show()

    def move_label(self, pos: list, current_pix_key: str) -> None:
        # metodo llamado por senal del backend

        curr_pix = self.pixmaps[current_pix_key]
        self.setPixmap(curr_pix)
        self.setScaledContents(True)
        self.move(*pos)
        self.raise_()
        self.show()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            # emitir de algun modo al backend
            print(f'> Clicked: {self.tipo}')

    def raise_label(self):
        self.raise_()


class ImmovableLabel(QLabel):
    """
    Entidad grafica de un bloque solido (pared, cañon)
    Utilizado para saber que tipo de bloque estamos colocando
    """

    def __init__(self, tipo: str, senal_pos: pyqtSignal, parent: QWidget, *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.tipo = tipo
        self.senal_pos = senal_pos

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            # emitir de algun modo al backend
            # print(f'> Clicked: {self.tipo}')
            x = self.x()
            y = self.y()
            self.senal_pos.emit(x, y)


class ItemLabel(QLabel):
    """
    Entidad grafica de un item de nuestro inventario
    """
    identificador = 1

    def __init__(self, parent: QWidget,
                 senal_selected: pyqtSignal,
                 pixmaps: dict,
                 tipo: str = 'No item',
                 *args, **kwargs) -> None:
        super().__init__(parent=parent, *args, **kwargs)
        self.identificador = ItemLabel.identificador
        ItemLabel.identificador += 1
        self.senal_selected = senal_selected
        self.pixmaps = pixmaps
        self.tipo = tipo
        self.default: str = 'No item'
        self.name = {'M': 'Manzana', 'CO': 'Congelador'}

    def place_pixmap(self, key: str):
        # cada item deberia poder colocarse en una posicion en base a su identificador
        self.setPixmap(self.pixmaps[key])
        self.setScaledContents(True)
        self.show()

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            try:
                print(f'> Item Seleccionado: {self.name[self.tipo]}')
                self.senal_selected.emit(self.identificador)
            except KeyError:
                print('> No item')

    def reset_item(self):
        # cuando se use un item o cuando se resete el inventario al morir
        self.tipo = self.default
        self.clear()
