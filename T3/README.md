# Tarea 3: DCCine 🎬🎥

## Consideraciones generales :octocat:
Mi tarea logra pasar todos los tests entregados

### Cosas implementadas y no implementadas :white_check_mark: :x:


####  Programación funcional
##### ✅ Utiliza 1 generador: Todas las funciones pasan los tests
##### ✅ Utiliza 2 generadores: Todas las funciones pasan los tests
##### ✅ Utiliza 3 o más generadores: Todas estas funciones pasan los tests. Ademas, todas ellas estan programadas con un estilo muy similar (en cada una se va poniendo que van haciendo las lineas, todo de manera muy secuencial), Para este punto habia ido a la programaton y ya le habia agarrado el hilo a la programacion funcional, por lo que las pude hacer sin mayor complicacion, en comparacion a los dos grupos de funciones anteriores.
####  API
##### ✅ Obtener información: Todas las funciones pasan los tests
##### ✅ Modificar información: Todas las funciones pasan los tests

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```peli.py```. Además se debe crear los siguientes archivos y directorios adicionales:


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```collections```
    - `namedTuple`. Estructura de datos base en esta tarea. Utilice las que entregaron, pero demas tuve que crear unas adicionales en la funcion `normalizar_fecha_de_Funcion` en `funciones_consultas`
    
    - ```Counter()```. Utilizada en `consultas.py`. Para realizar conteos de frecuencia, mas simple. El uso de sus metodos fueron autorizados (fuente [issue #438](https://github.com/IIC2233/Syllabus/issues/438#issuecomment-1817489845))

2. ```itertools```: 
    - `product()`: Utilizada en `consultas.py`. Para realizar productos cartesiamos entre las `namedTuple` entregadas. Con el objetivo de ser usadas en filtros en varias funciones.

3. `functools`: Utilizada en `consultas.py`
    - `reduce()`: Utilizada en `consultas.py`. Funcion que forma parte de los contenidos del curso.

4. `math`:
    - `ceil()`: Funcion usada en `edad_promedio` en `consultas.py`. Para poder aproximar por techo la edad promedio de las personas.

5. `datetime`:
    - `datetime`: Funcion usada en las funcion `crear_fecha_datetime` en `funciones_consulta.py`. Usada solamente para poder realizar comparaciones entre fechas para la funcion `personas_no_asisten` en `consultas.py`

6. `requests`: para el intercambio de informacion  con la API
### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. `funciones_consulta`. **tl;dr: Son funciones para acortar el archivo principal**. Contiene funciones encargadas de realizar comparaciones simples entre datos, crear objetos de apoyo (`datetime` por ejemplo) o mostrar los resultados de algunas funciones que retornaban strings largos de textos. En el archivo se encuentra comentado que funcion de `consultas.py` utiliza cierta funcion de esta libreria.
    - `normalizar_fecha_de_Funcion`
    - `comparador_titulo_rating`
    - `comparador_rating`
    - `comparador_por_rating_y_posicion`
    - `comparador_pos`
    - `format_fecha`
    - `resultado_genero_comun`
    - `resultado_edad_promedio`
    - `obtener_total_reservas`
    - `crear_fecha_datetime`
    - `comparar_fechas`
    - `reservas`

## Supuestos y consideraciones adicionales :thinking:
1. ***SOBRE LA PARTE DE LA API***: Los metodos realizados en esta parte son muy parecidos, por no decir iguales, a los de la AC5. Para que lo tengan en consideracion en caso de que salga cualquier alerta de copia

## Referencias de código externo :book:
Para esta tarea no necesite de codigo externo

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).