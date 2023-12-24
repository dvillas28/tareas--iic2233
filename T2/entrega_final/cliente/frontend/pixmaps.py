from PyQt6.QtGui import QPixmap
from frontend import parametros_frontend as p
from os.path import join


def load_pixmaps() -> dict:
    """
    Carga los objetos QPixmap presentes en el juego que luego seran enviados al frontend
    Cada elemento del diccionario es a su vez un diccionario con los QPixmaps especificos de cada
    elemento grafico del tablero
    """
    # diccionario principal
    pix = {}

    # TILES
    tiles_pix = {}
    tiles_pix['-'] = QPixmap(join(*(p.BLOQUE_FONDO.split('/'))))
    tiles_pix['P'] = QPixmap(join(*(p.BLOQUE_PARED.split('/'))))

    # CAÑON
    canon_pix = {}
    canon_pix['CU'] = QPixmap(join(*(p.CANON_ARRIBA.split('/'))))
    canon_pix['CD'] = QPixmap(join(*(p.CANON_ABAJO.split('/'))))
    canon_pix['CL'] = QPixmap(join(*(p.CANON_IZQUIERDA.split('/'))))
    canon_pix['CR'] = QPixmap(join(*(p.CANON_DERECHA.split('/'))))

    # CONEJO
    conejo_pix = {}
    conejo_pix['C'] = QPixmap(join(*(p.CONEJO.split('/'))))

    # CONEJO_ARRIBA
    conejo_pix['C_U_1'] = QPixmap(join(*(p.CONEJO_ARRIBA_1.split('/'))))
    conejo_pix['C_U_2'] = QPixmap(join(*(p.CONEJO_ARRIBA_2.split('/'))))
    conejo_pix['C_U_3'] = QPixmap(join(*(p.CONEJO_ARRIBA_3.split('/'))))

    # CONEJO ABAJO
    conejo_pix['C_D_1'] = QPixmap(join(*(p.CONEJO_ABAJO_1.split('/'))))
    conejo_pix['C_D_2'] = QPixmap(join(*(p.CONEJO_ABAJO_2.split('/'))))
    conejo_pix['C_D_3'] = QPixmap(join(*(p.CONEJO_ABAJO_3.split('/'))))

    # CONEJO IZQUIERDA
    conejo_pix['C_L_1'] = QPixmap(join(*(p.CONEJO_IZQUIERDA_1.split('/'))))
    conejo_pix['C_L_2'] = QPixmap(join(*(p.CONEJO_IZQUIERDA_2.split('/'))))
    conejo_pix['C_L_3'] = QPixmap(join(*(p.CONEJO_IZQUIERDA_3.split('/'))))

    # CONEJO DERECHA
    conejo_pix['C_R_1'] = QPixmap(join(*(p.CONEJO_DERECHA_1.split('/'))))
    conejo_pix['C_R_2'] = QPixmap(join(*(p.CONEJO_DERECHA_2.split('/'))))
    conejo_pix['C_R_3'] = QPixmap(join(*(p.CONEJO_DERECHA_3.split('/'))))

    # items/efectos
    item_pix = {}
    item_pix['M'] = QPixmap(join(*(p.MANZANA.split('/'))))
    item_pix['BM'] = QPixmap(join(*(p.MANZANA_BURBUJA.split('/'))))
    item_pix['EX'] = QPixmap(join(*(p.EXPLOSION.split('/'))))
    item_pix['CO'] = QPixmap(join(*(p.CONGELACION.split('/'))))
    item_pix['BC'] = QPixmap(join(*(p.CONGELACION_BURBUJA.split('/'))))

    # LOBO HORIONZAL
    lobo_h_pix = {}
    lobo_h_pix['LH_R_1'] = QPixmap(join(*(p.LOBO_DERECHA_1.split('/'))))
    lobo_h_pix['LH_R_2'] = QPixmap(join(*(p.LOBO_DERECHA_2.split('/'))))
    lobo_h_pix['LH_R_3'] = QPixmap(join(*(p.LOBO_DERECHA_2.split('/'))))

    lobo_h_pix['LH_L_1'] = QPixmap(join(*(p.LOBO_IZQUIERDA_1.split('/'))))
    lobo_h_pix['LH_L_2'] = QPixmap(join(*(p.LOBO_IZQUIERDA_2.split('/'))))
    lobo_h_pix['LH_L_3'] = QPixmap(join(*(p.LOBO_IZQUIERDA_3.split('/'))))

    # LOBO VERTICAL
    lobo_v_pix = {}
    lobo_v_pix['LV_D_1'] = QPixmap(join(*(p.LOBO_VERTICAL_ABAJO_1.split('/'))))
    lobo_v_pix['LV_D_2'] = QPixmap(join(*(p.LOBO_VERTICAL_ABAJO_2.split('/'))))
    lobo_v_pix['LV_D_3'] = QPixmap(join(*(p.LOBO_VERTICAL_ABAJO_3.split('/'))))

    lobo_v_pix['LV_U_1'] = QPixmap(
        join(*(p.LOBO_VERTICAL_ARRIBA_1.split('/'))))
    lobo_v_pix['LV_U_2'] = QPixmap(
        join(*(p.LOBO_VERTICAL_ARRIBA_2.split('/'))))
    lobo_v_pix['LV_U_3'] = QPixmap(
        join(*(p.LOBO_VERTICAL_ARRIBA_3.split('/'))))

    # ZANAHORIA
    zanahoria_pix = {}
    zanahoria_pix["ZU"] = QPixmap(join(*(p.ZANAHORA_ARRIBA.split('/'))))
    zanahoria_pix["ZD"] = QPixmap(join(*(p.ZANAHORA_ABAJO.split('/'))))
    zanahoria_pix["ZL"] = QPixmap(join(*(p.ZANAHORA_IZQUIERDA.split('/'))))
    zanahoria_pix["ZR"] = QPixmap(join(*(p.ZANAHORA_DERECHA.split('/'))))

    # añadimos todos los subdiccionarios a al diccionario principal
    pix['tiles'] = tiles_pix
    pix['conejo'] = conejo_pix
    pix['canon'] = canon_pix
    pix['items'] = item_pix
    pix['lobo_h'] = lobo_h_pix
    pix['lobo_v'] = lobo_v_pix
    pix['zanahoria'] = zanahoria_pix

    return pix
