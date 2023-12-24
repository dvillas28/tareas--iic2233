from PyQt6.QtCore import QObject
from backend.logica_utils import parametros as p


class Entity(QObject):
    """
    Clase "abstracta" de una entidad logica
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def x_tab(self, x: int) -> int:
        """
        Retorna la equivalente de x en el tablero de la posicion
        """
        return x * p.TAMAÑO_BLOQUE + p.PADDING_MENU

    def y_tab(self, y: int) -> int:
        """
        Retorna la equivalente de y en el tablero de la posicion
        """
        return y * p.TAMAÑO_BLOQUE

    # @abstractmethod
    def spawn(self) -> None:
        pass

    # @abstractmethod
    def move(self) -> None:
        pass

    # @abstractmethod
    def pause(self) -> None:
        pass
