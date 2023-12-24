from typing import Any


class Mensaje():
    def __init__(self, orden: str, contenido: Any) -> None:
        self.orden = orden
        self.contenido = contenido
