
import collections
import datetime
import functools
import itertools
import math
import utilidades

from typing import Generator
import funciones_consultas as fc


# utilizan 1 generador
def peliculas_genero(generador_peliculas: Generator, genero: str):
    filtrado = filter(lambda peli: peli.genero == genero, generador_peliculas)
    return filtrado


def personas_mayores(generador_personas: Generator, edad: int):
    filtrado = filter(lambda persona: persona.edad >= edad, generador_personas)
    return filtrado


def funciones_fecha(generador_funciones: Generator, fecha: str):

    filtrado_1900 = filter(lambda func: int(
        func.fecha[-2:]) >= 24, generador_funciones)  # peliculas del 1900
    filtrado_2000 = filter(lambda func: int(
        func.fecha[-2:]) < 24, generador_funciones)  # peliculas del 2000

    centenio = fecha[6:8]

    # le quitamos el centenio al año de la fecha
    fecha_formatted = f'{fecha[:2]}-{fecha[3:5]}-{fecha[-2:]}'

    if centenio == '19':
        filtrado = filter(lambda func: func.fecha ==
                          fecha_formatted, filtrado_1900)

    elif centenio == '20':
        filtrado = filter(lambda func: func.fecha ==
                          fecha_formatted, filtrado_2000)
    return filtrado


def titulo_mas_largo(generador_peliculas: Generator) -> str:

    pelicula = functools.reduce(
        lambda p1, p2: fc.comparador_titulo_rating(p1, p2), generador_peliculas)

    return pelicula.titulo


def normalizar_fechas(generador_funciones: Generator):
    mapeo = map(fc.normalizar_fecha_de_Funcion, generador_funciones)
    return mapeo


def personas_reservas(generador_reservas: Generator):
    set_reservas = {reserva.id_persona for reserva in generador_reservas}
    return set_reservas


def peliculas_en_base_al_rating(generador_peliculas: Generator,
                                genero: str, rating_min: int, rating_max: int):
    filtro = filter(lambda peli: peli.genero == genero and (
        rating_min <= peli.rating <= rating_max), generador_peliculas)
    return filtro


def mejores_peliculas(generador_peliculas: Generator):
    lista_peliculas = [peli for peli in generador_peliculas]

    lista_peliculas.sort(key=lambda p: p.id)
    lista_peliculas.sort(key=lambda p: p.rating, reverse=True)

    if len(lista_peliculas) > 20:
        return lista_peliculas[:20]
    else:
        return lista_peliculas


def pelicula_genero_mayor_rating(generador_peliculas: Generator, genero: str) -> str:
    # lista global de peliculas
    lista_peliculas = [peli for peli in generador_peliculas]

    peliculas_con_ese_genero = filter(
        lambda peli: peli.genero == genero, generador_peliculas)

    mejores_con_ese_genero = mejores_peliculas(peliculas_con_ese_genero)

    if mejores_con_ese_genero:
        pelicula = functools.reduce(
            lambda p1, p2: fc.comparador_por_rating_y_posicion(
                p1, p2, lista_peliculas),
            mejores_con_ese_genero)

        return pelicula.titulo

    else:
        return ""


# utilizan dos generadores
def fechas_funciones_pelicula(generador_peliculas: Generator, generador_funciones: Generator,
                              titulo: str):
    # buscamos primero la tupla de la pelicula que queremos
    pelicula = functools.reduce(
        lambda p1, _: p1 if p1.titulo == titulo else _, generador_peliculas)

    if pelicula.titulo != titulo:  # no esta la pelicula
        # esto es para retornar el generador vacio
        return filter(lambda p: p.titulo == titulo, generador_peliculas)

    # luego filtramos donde cuadre el id de la pelicula con la funcion
    filtro_funciones = filter(
        lambda func: func.id_pelicula == pelicula.id, generador_funciones)

    # luego mapeamos todo eso para solo entregar la fecha
    mapeo_fechas = map(lambda func: func.fecha, filtro_funciones)
    return mapeo_fechas


def genero_mas_transmitido(generador_peliculas: Generator, generador_funciones: Generator,
                           fecha: str) -> str:
    # primero debemos normalizar ambos formatos de fecha
    funciones_normalizadas = normalizar_fechas(generador_funciones)
    nueva_fecha = fc.format_fecha(fecha)

    # ahora debemos recopilar las funciones en esa fecha
    funciones_filtradas_por_fecha = filter(lambda func: func.fecha ==
                                           nueva_fecha, funciones_normalizadas)

    # obtenemos los ids de esas funciones con un map
    ides = [ide for ide in map(lambda func: func.id_pelicula,
                               funciones_filtradas_por_fecha)]

    # por cada id, quiero el genero asociado a la pelicula asociada a ese id
    peliculas = [peli for peli in generador_peliculas]
    generos = [peli.genero for ide in ides for peli in peliculas if peli.id == ide]
    contador = collections.Counter(generos)

    if contador.most_common(1):  # vemos si existe el mas comun
        return contador.most_common(1)[0][0]
    else:
        return ""


def id_funciones_genero(generador_peliculas: Generator, generador_funciones: Generator,
                        genero: str):
    # tomamos las peliculas que coincidan con el genero
    pelis_genero = [peli for peli in filter(
        lambda p: p.genero == genero, generador_peliculas)]

    # en base a esos ids, obtener todas las funciones posibles
    lista_func = [func for func in generador_funciones]

    # realizarmos el filtrado con una comprension
    lista = [
        func.id for peli in pelis_genero for func in lista_func if func.id_pelicula == peli.id]

    return lista


def butacas_por_funcion(generador_reservas: Generator, generador_funciones: Generator,
                        id_funcion: int) -> int:

    # buscamos la funcion asociada a ese id
    a = [1 for butaca in generador_reservas if butaca.id_funcion == id_funcion]
    return len(a)


def salas_de_pelicula(generador_peliculas: Generator, generador_funciones: Generator,
                      nombre_pelicula: str):
    # revisamos si existe
    # si existe tomamos su id y filtramos
    # buscamos primero la tupla de la pelicula que queremos

    pelicula = functools.reduce(
        lambda p1, _: p1 if p1.titulo == nombre_pelicula else _, generador_peliculas)

    if pelicula.titulo != nombre_pelicula:  # no esta la pelicula
        # esto es para retornar el generador vacio
        return filter(lambda p: p.titulo == nombre_pelicula, generador_peliculas)

    n_salas = [
        func.numero_sala for func in generador_funciones if func.id_pelicula == pelicula.id]

    return n_salas


# utilizan 3 o mas generadores
def nombres_butacas_altas(generador_personas: Generator, generador_peliculas: Generator,
                          generador_reservas: Generator, generador_funciones: Generator,
                          titulo: str, horario: int):

    # con generador peliculas tomar, la que coincida con el nombre
    pelicula = [p for p in filter(
        lambda p: p.titulo == titulo, generador_peliculas)][0]

    # luego con generador funciones, tomar la funcio  que coincidia con esa pelicula y esa funcion
    funcion = [f for f in filter(lambda func: func.horario ==
                                 horario and func.id_pelicula == pelicula.id,
                                 generador_funciones)][0]

    # con el id de esa funion y generador reservas, tomar las reservas que coincidad con ese id
    id_personas = [r.id_persona for r in filter(
        lambda reser: reser.id_funcion == funcion.id, generador_reservas)]

    # juntar en tuplas (id, persona)
    producto = itertools.product(id_personas, generador_personas)

    # con esas id tomar los nombres de las personas
    personas = [p[1].nombre for p in filter(
        lambda tup: tup[0] == tup[1].id, producto)]
    return personas


def nombres_persona_genero_mayores(generador_personas: Generator, generador_peliculas: Generator,
                                   generador_reservas: Generator, generador_funciones: Generator,
                                   nombre_pelicula: str, genero: str, edad: int):
    # obtenemos la pelicula
    pelicula = [p for p in filter(
        lambda p: p.titulo == nombre_pelicula, generador_peliculas)][0]

    # con el id de la pelicula, vemos todas las funciones que la publicaron
    funciones = [f for f in filter(
        lambda func: func.id_pelicula == pelicula.id, generador_funciones)]

    # hacemos el producto carteasiano entre las reservas y las funciones
    producto = itertools.product(funciones, generador_reservas)

    # tomamos todas las personas que fueron a una funcion de esa pelicula
    id_personas = [tup[1].id_persona for tup in filter(
        lambda tup: tup[0].id == tup[1].id_funcion, producto)]

    # emparejamos todos los id con una persona
    producto2 = itertools.product(generador_personas, id_personas)
    # vemos si coincide el id si coincen las condiciones dadas
    personas = {p[0].nombre for p in filter(
        lambda tup: tup[0].id == tup[1], producto2) if p[0].edad >= edad and p[0].genero == genero}

    return personas


def genero_comun(generador_personas: Generator, generador_peliculas: Generator,
                 generador_reservas: Generator, generador_funciones: Generator,
                 id_funcion: int) -> str:
    # Completar
    # tomamos la funcion que coincide con del id
    funcion = [f for f in filter(
        lambda func: func.id == id_funcion, generador_funciones)][0]

    # con la funcion indicada, tomamos el titulo de la pelicula
    pelicula = [p for p in filter(
        lambda peli: peli.id == funcion.id_pelicula, generador_peliculas)][0]

    # con la funcion indicada, tomamos todas reservas a esa funcion
    reservas = [r for r in filter(
        lambda reser: reser.id_funcion == funcion.id, generador_reservas)]

    # con las reservas, tomamos a todas las personas
    producto = itertools.product(generador_personas, reservas)
    # todas las personas que fueron a esa funcion
    personas = [tup[0] for tup in filter(
        lambda tup: tup[0].id == tup[1].id_persona, producto)]

    # con las personas, mapeamos su genero
    generos = [genre for genre in map(lambda p: p.genero, personas)]

    # realizamos un conteo
    counter = collections.Counter(generos)

    # retornamos el resultado
    return fc.resultado_genero_comun(id_funcion, pelicula.titulo, counter)


def edad_promedio(generador_personas: Generator, generador_peliculas: Generator,
                  generador_reservas: Generator, generador_funciones: Generator,
                  id_funcion: int) -> str:
    # tomamos la funcion que coincide con del id
    funcion = [f for f in filter(
        lambda func: func.id == id_funcion, generador_funciones)][0]

    # con la funcion indicada, tomamos a la pelicula
    pelicula = [p for p in filter(
        lambda peli: peli.id == funcion.id_pelicula, generador_peliculas)][0]

    # con la funcion indicada, tomamos todas reservas a esa funcion
    reservas = [r for r in filter(
        lambda reser: reser.id_funcion == funcion.id, generador_reservas)]

    # con las reservas, tomamos a todas las personas
    producto = itertools.product(generador_personas, reservas)
    # todas las personas que fueron a esa funcion
    personas = [tup[0] for tup in filter(
        lambda tup: tup[0].id == tup[1].id_persona, producto)]

    edad_prom = sum([p.edad for p in personas])/len(personas)
    return fc.resultado_edad_promedio(id_funcion, pelicula.titulo, math.ceil(edad_prom))


def obtener_horarios_disponibles(generador_peliculas: Generator, generador_reservas: Generator,
                                 generador_funciones: Generator, fecha_funcion: str,
                                 reservas_maximas: int):
    # tomamos todas las peliculas que se dan ese ese dia
    lista_funciones = [f for f in generador_funciones]
    funciones = [p for p in filter(
        lambda peli: peli.fecha == fecha_funcion, lista_funciones)]

    # tomamos la pelicula con mayor rating en esa fecha
    # debemos asociar cada una de las funciones a su pelicula
    producto = itertools.product(funciones, generador_peliculas)
    func_peli_esa_fecha = [tupla for tupla in filter(
        lambda tup: tup[0].id_pelicula == tup[1].id, producto)]

    # ahora, de todas las peliculas en esa fecha, tomamos la que tiene mas alto rating
    func_peli_esa_fecha.sort(key=lambda tupla: tupla[1].rating, reverse=True)
    pelicula = func_peli_esa_fecha[0][1]

    # luego con esa pelicula, vemos todas las funciones donde den solo esa pelicula
    funciones_pelicula = [peli_func[0]
                          for peli_func in func_peli_esa_fecha if peli_func[1].id == pelicula.id]

    # por cada funcion donde den esa pelicula, hay que sacar todas las reservas que existen
    # si el total de reservas de una funcion exceden el maximo, entonces esa funcion esta llena
    # si no, añadimos el horario de la funcion

    lista_reservas = [r for r in generador_reservas]
    horarios = {f.horario for f in funciones_pelicula if fc.obtener_total_reservas(
        f, lista_reservas) < reservas_maximas}

    return horarios


def personas_no_asisten(generador_personas: Generator, generador_reservas: Generator,
                        generador_funciones: Generator, fecha_inicio: str, fecha_termino: str):
    # primero normalizamos todos los str de las fechas a dd-mm-yyyy
    funciones_normalizadas = normalizar_fechas(generador_funciones)
    fecha_ini = fc.format_fecha(fecha_inicio)
    fecha_end = fc.format_fecha(fecha_termino)

    # tomamos todas las funciones que estan dentro del rango
    funciones_dentro_rango = [f for f in filter(
        lambda func: fc.comparar_fechas(fecha_ini, fecha_end, func.fecha), funciones_normalizadas)]

    # por cada funcion, vemos las reservas asociadas a ella
    lista_reservas = [r for r in generador_reservas]

    # crearemos una lista de id de personas que hiciceron una reserva a las peliculas
    # cada elemento de esta lista es una lista con los id de las personas que reservaron para esa
    # funcion
    mapeo_reservas = [l for l in map(lambda func: fc.reservas(
        lista_reservas, func), funciones_dentro_rango)]

    # desenpaquetamos todas las id en una sola lista grande
    # en esta lista se encuentran los ids de todas las personas que reservaron para cualquier
    # funcion dentro del rango
    reservas_dentro_de_rango = [
        i for sublista in mapeo_reservas for i in sublista]

    # luego necitamos añadir a las personas que NO aparecen en la lista de ids
    # estas personas
    # 1. no aparecian antes las reservas (jamas hiciceron una reserva en 1er lugar)
    # 2, si es que tenian una reserva, esta fue fuera de rango y por lo tanto no logro entrar
    # en el mapeo de reservas
    personas = [p for p in filter(
        lambda per: per.id not in reservas_dentro_de_rango, generador_personas)]

    return personas


if __name__ == '__main__':
    pass
