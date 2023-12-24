# Tarea 1: DCChexxploding 💥♟️

Mi tarea ***consigue pasar todos los tests cases entregados***. Cada funcion y metodo se encuentra con una pequeña descripcion de que es lo que hace.

### Cosas implementadas y no implementadas :white_check_mark: :x:


#### ✅ Parte 2 - Menú: 18 pts (30%)
##### ✅ Consola: Hecha completa. El modo de la ejecucion por consola se encuentra en la seccion 'Ejecución'.
##### ✅ Menú de Acciones: Hecha completa. Ciclo `while` donde cada iteración muestra el menú y el programa se queda a esperar a que opcion se entrega. Se imprime una linea que indica al usuario la opcion que eligió (`> opcion_elegida`).
##### ✅ Modularización: funciones que comprueban datos, obtienen *id's*, etc,  se encuentran en el modulo `misc_functions` . Con esto se logra que en los archivos `main.py` y `menu.py` se logre seguir de una manera mas clara el flujo del programa en lo que respecta al menú.
##### ✅ PEP8: segun el linter que tengo instalado, no hubo violaciones al PEP8 en estos archivos.

## Ejecución :computer:
EL modulo principal de la tarea a ejecutar es `main.py`.

```
python3 main.py user_name tablero_name
```
Donde `user_name` y `tablero_name` son argumentos necesarios para la ejecucion del menú del programa.



## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```copy```: ```copy()``` y ```deepcopy()``` / utilizadas en ``solver.py``y ``tablero.py`` para poder copiar listas y en algunos casos, **copiar tambien los elementos de la lista**. Use ```deepcopy``` en una funcion recursiva para no ir alterando a una lista que se utiliza como argumento, a medida que iba corriendo la recursion, de lo contrario, no se retornaban todas las soluciones posibles.
### Librerías propias
Los modulos que creé son los siguentes:

1. ```misc_functions```: Contiene una variedad de funciones utilizadas en `main.py`, `menu.py` y `tablero.py`. Son funciones que recuperan/limpian datos, comprueban condiciones, obtienen *id's*. etc, en partes del código asociadas al menu principal del programa. Son `archivo_a_lista()`, `existe_tablero()`, `get_id_tablero`, `ingresar_datos()`, y `crear_tablero()`.

2. ```tablero_functions```: Contiene funciones utilizadas en `tablero.py`. La gran mayoria de estas ocultan la funcionalidad de los metodos de `Tablero`. Creada para no llenar de codigo a la clase.
La gran mayoria de las funciones iteran sobre el tablero para entregarnos informacion de utilidad,
como alguna fila, columna o diagonal. Son `get_peones_invalidos()`, `get_columna()`, `get_diagonal()`, `alcance_horizontal()` y `get_piezas_explosivas`.

3. ```solver```: Contiene funciones que involucradas en la resolución del tablero al llamar al método `solucionar()`. Son `get_celdas_vacias()`, `solver_recursivo()`, `aplicar_cambios()`, `condicion_solucion()` y `esta_el_tablero_resuelto()`.

## Supuestos y consideraciones adicionales :monocle_face:
Los supuestos que realicé durante la tarea son los siguientes:

### Sobre el menú

1. Se asume que solo se ingresarán dos argumentos en consola, de lo contrario, el programa tira error.

2. Al seleccionar la opcion de "limpiar tablero" en el menú, solamente se imprime un mensaje, 
para ver los resultados de la limpieza, se debe usar la opcion de "mostrar el tablero". Lo hice de esa manera ya que el enunciado no especifica que haya que imprimir el tablero despues de limpiarlo, pero añadi el mensaje para asegurarle al usuario que el tablero fue limpiado.

3. Al seleccionar la opcion de "solucionar tablero", se imprime un mensaje, el tablero se soluciona y finalmente se imprime. Me di cuenta que **en el caso de tableros que no tengan solucion, la funcion entregada `imprimir_tablero()` genera errores para listas vacias**, por lo que en el codigo se deja claro que los llamados a `imprimir_tablero()` se haran **solo si la solucion entregada no es una lista vacia**, imprimiendo una directamente en el caso contrario. De manera similar que en el punto 1., el enunciado no especifica si se debe imprimir el tablero, pero como la opcion 1 ("mostrar tablero") **solo muestra el tablero original, este limpio de peones o no**, considere que era necesario imprimirlo en su estado resuelto al seleccionar esta opción. 

### Sobre la clase `Tablero` y sus modulos importados

1. Existen funciones donde algunos de parametros no tiene el tipo especificado, siendo la gran mayoria funciones que reciben a una instancia de la clase `Tablero`. Esto porque el tratar de importar la clase en esos modulos, que a su vez son importados por la misma clase, daba error. Para estas funciones se asume que cualquier parametro llamado `tablero` sera una instancia de esa clase, siendo el caso contrario cuando se refiere al atributo ```Tablero.tablero``` donde ese caso su tipo se especifica como `list`.

## Referencias de código externo :book::eyes:

Para realizar mi tarea saqué código de:
1. [GeeksforGeeks - Check if two elements of a matrix are on the same diagonal or not](https://www.geeksforgeeks.org/check-if-two-elements-of-a-matrix-are-on-the-same-diagonal-or-not/). Muestra una forma para poder saber si 2 elementos de una matriz de encuentran en la misma diagonal, en base a su posición (la suma/resta de las coodenadas `x, y` deben de ser iguales), una forma esta implementada en el archivo ``pieza_explosiva.py`` en las líneas 42-48. 

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).
