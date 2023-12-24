from PyQt6.QtCore import QUrl
from frontend import parametros_frontend as p
from os.path import join


def load_sounds() -> dict:
    sound_dict = {}

    lose = QUrl.fromLocalFile(join(*(p.DERROTA_WAV.split('/'))))
    win = QUrl.fromLocalFile(join(*(p.VICTORIA_WAV.split('/'))))

    sound_dict['derrota'] = lose
    sound_dict['victoria'] = win

    return sound_dict
