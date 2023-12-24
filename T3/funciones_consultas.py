from utilidades import Funciones, Peliculas
from collections import namedtuple, Counter
from datetime import datetime


# usada por normalizar_fechas
def normalizar_fecha_de_Funcion(func: namedtuple) -> namedtuple:
    """
    Recibe una instancia de Funciones y retorna ua instancia de Funciones, 
    pero con el atributo de fecha normalizado
    """

    # retorna una tupla de atributos nuevos
    ide = func.id
    numero_sala = func.numero_sala
    id_pelicula = func.id_pelicula
    horario = func.horario
    fecha = func.fecha

    dia = fecha[:2]
    mes = fecha[3:5]
    año = fecha[-2:]

    if int(año) >= 24:
        new_fecha = f'19{año}-{mes}-{dia}'
    elif int(año) < 24:
        new_fecha = f'20{año}-{mes}-{dia}'

    return Funciones(ide, numero_sala, id_pelicula, horario, new_fecha)


# usada por titulo_mas_largo
def comparador_titulo_rating(peli_1: namedtuple, peli_2: namedtuple) -> namedtuple:
    # compara el largo
    # print(f'Comparando {peli_1.titulo} con {peli_2.titulo}')
    if len(peli_1.titulo) == len(peli_2.titulo):
        # si el largo es el mismo, compara el rating
        # print('Son del mismo largo')
        return comparador_rating(peli_1, peli_2)

    elif len(peli_1.titulo) > len(peli_2.titulo):
        # print(f'{peli_1.titulo} es mas largo')
        return peli_1

    elif len(peli_1.titulo) < len(peli_2.titulo):
        # print(f'{peli_2.titulo} es mas largo')
        return peli_2


# usada por titulo_mas_largo
def comparador_rating(peli_1: namedtuple, peli_2: namedtuple) -> namedtuple:
    # print(
    #     f'Comparando {peli_1.titulo}: {peli_1.rating} con {peli_2.titulo}: {peli_2.rating')
    if peli_1.rating == peli_2.rating:
        # print(f'Mismo rating, retornando {peli_2.titulo}')
        return peli_2

    elif peli_1.rating > peli_2.rating:
        # print(f'{peli_1.titulo} tiene mas rating')
        return peli_1

    elif peli_1.rating < peli_2.rating:
        # print(f'{peli_2.titulo} tiene mas rating')
        return peli_2


# Usada por pelicula_genero_mayor_rating
def comparador_por_rating_y_posicion(peli_1: namedtuple, peli_2: namedtuple,
                                     lista_pelis) -> namedtuple:
    # comparar por rating, si es el mismo comparar por id
    if peli_1.rating == peli_2.rating:
        return comparador_pos(peli_1, peli_2, lista_pelis)

    elif peli_1.rating > peli_2.rating:
        return peli_1

    elif peli_1.rating < peli_2.rating:
        return peli_2


# Usada por pelicula_genero_mayor_rating
def comparador_pos(peli_1: namedtuple, peli_2: namedtuple, lista_pelis):
    # retorna la tupla que este en la menor posicion
    pos_peli_1 = lista_pelis.index(peli_1)
    pos_peli_2 = lista_pelis.index(peli_2)

    if pos_peli_1 < pos_peli_2:
        return peli_1
    else:
        return peli_2


# utilizada por genero_mas_transmitido, personas_no_asisten
def format_fecha(fecha: str) -> str:
    """
    Cambia el formato de la fecha DD-MM-AAAA -> AAAA-MM-DD
    """
    dia = fecha[:2]
    mes = fecha[3:5]
    ano = fecha[-4:]

    return f'{ano}-{mes}-{dia}'


# utilizada por genero_comun
def resultado_genero_comun(id_func: int, name_peli: str, generos: Counter) -> str:
    base = f'En la función {id_func} de la película {name_peli} '
    mas_comunes = generos.most_common(3)
    # print(mas_comunes)

    if len(mas_comunes) == 3:
        if mas_comunes[0][1] == mas_comunes[1][1] == mas_comunes[2][1]:
            # 3 iguales
            full_result = f'se obtiene que la cantidad de personas es igual para todos los géneros.'

        elif mas_comunes[0][1] == mas_comunes[1][1] and mas_comunes[0][1] != mas_comunes[2][1]:
            # 2 iguales
            result1 = f'se obtiene que la mayor parte del público es de {mas_comunes[0][0]} y '
            result2 = f'{mas_comunes[1][0]} con la misma cantidad de personas.'
            full_result = result1 + result2

        elif mas_comunes[0][1] != mas_comunes[1][1] and mas_comunes[0][1] != mas_comunes[2][1]:
            # 1 igual
            full_result = f'la mayor parte del público es {mas_comunes[0][0]}.'

    elif len(mas_comunes) == 2:

        if mas_comunes[0][1] == mas_comunes[1][1]:
            # 2 iguales
            result1 = f'se obtiene que la mayor parte del público es de {mas_comunes[0][0]} y '
            result2 = f'{mas_comunes[1][0]} con la misma cantidad de personas.'
            full_result = result1 + result2

        else:
            # 1 igual
            full_result = f'la mayor parte del público es {mas_comunes[0][0]}.'

    elif len(mas_comunes) == 1:
        # 1 igual
        full_result = f'la mayor parte del público es {mas_comunes[0][0]}.'

    return base + full_result


# usada por edad_promedio
def resultado_edad_promedio(id_func: int, name_peli: str, prom: int) -> str:
    base = 'En la función {} de la película {} la edad promedio del público es {}.'
    return base.format(id_func, name_peli, prom)


# usada por obtener_horarios_disponibles
def obtener_total_reservas(funcion: namedtuple, lista_reservas) -> int:
    reservas = [
        1 for reserv in lista_reservas if reserv.id_funcion == funcion.id]

    return sum(reservas)


# usada por personas_no_asisten
def crear_fecha_datetime(fecha_en_dd_mm_yyyy: str) -> datetime:
    # date: datetime(año, mes, dia)
    ano = int(fecha_en_dd_mm_yyyy[:4])
    mes = int(fecha_en_dd_mm_yyyy[5:7])
    dia = int(fecha_en_dd_mm_yyyy[-2:])

    return datetime(ano, mes, dia)


# usada por personas_no_asisten
def comparar_fechas(fecha_ini: str, fecha_end: str, fecha: str) -> bool:
    datetime_interes = crear_fecha_datetime(fecha)
    datetime_inicio = crear_fecha_datetime(fecha_ini)
    datetime_final = crear_fecha_datetime(fecha_end)

    return datetime_inicio <= datetime_interes <= datetime_final


# usada por personas_no_asisten
def reservas(lista_reservas, funcion: namedtuple):
    return [r.id_persona for r in filter(lambda res: res.id_funcion == funcion.id, lista_reservas)]
