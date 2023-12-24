# Tarea 2: DCConejoChico 🐇💨

## Consideraciones generales :octocat:

El programa es jugable, logré terminar todo lo que se pedia en el enunciado

El programa, en primera instancia y hasta donde lo logre probar, *deberia* funcionar en Linux y Windows, pero considerar que fue la tarea la fui desarrollando en un ambiente de WSL, asi que en cualquier caso de una posible no ejecucion en Windows, porfavor ejecutarlo en **Linux**. 

Ante cualquier duda del funcionamiento y el porque de algunas *features* del juego, por favor revisar los [Supuestos y Consideraciones Adicionales](#supuestos-y-consideraciones-adicionales-🤔)

### Cosas implementadas y no implementadas :white_check_mark: :x:

#### Entrega Final: 46 pts (75%)

##### ✅ Ventana Inicio: La ventana funciona correctamente, el servidor envia una lista con los 5 mejores puntajes, que luego el backend se encarga de gestionar para mostrar en el salón de la fama

##### ✅ Ventana Juego: Estan todos los elementos pedidos, cada nivel tiene su tiempo determinado y velocidades determinadas para los lobos

##### ✅ ConejoChico: El conejo se mueve correctamente y responde bien frente a colisiones con lobos y zanahorias. La clase `Player` cuenta con metodos para moverse, las animaciones de moviemento basado en que tecla fue presionada. Las vidas del jugador y las colisiones con otras entidades son gestionadas por el backend `LogicaJuego` (en el metodo `player_hit` y las colisiones en el metodo `handle_colision`)

##### ✅ Lobos: Los lobos horizontales y verticales funcionan bien, cada instancia de `Lobo` tiene su propio `QTimer` que se encarga de indicarle la posicion en el tablero y la rotacion de imagenes que se deben colocar por el frontend

##### ✅ Cañón de Zanahorias: El cañon dispara zanahorias cada 3 segundos (valor colocado en `parametros.py`). Las zanahorias desaparecen correctamente al colisionar con alguna pared. Cada objeto `Canon` se encarga de lanzar sus propios objetos `Zanahoria`

##### ✅ Bomba Manzana: La bomba de manzana funciona correctamente. Es capaz de eliminar lobos que se encuentren en su alcance, o que lleguen a este moviendose. Info mas detallada en [los supuestos](#supuestos-y-consideraciones-adicionales-🤔)

##### ✅ Bomba Congeladora: la bomba congelador funciona correctamente, es capaz de ralentizar a los lobos que se encuentren en su alcance, ademas de al jugador. Ademas sus efetcos se mantienes durante todo el nivel, y solo se acaban cuando el jugador logre terminarlo. Info mas detallada en [los supuestos](#supuestos-y-consideraciones-adicionales-🤔)

##### ✅ Fin del nivel: Las dos formas de acabar un nivel es perdiendo todas las vidas, o superando el nivel. Cada vez que se supera un nivel, el cliente envia los datos del usuario (el envio de datos se realiza en `LogicaJuego` hacia `Cliente`, quien luego de encodificar y encriptar, envia el mensaje), y es el servidor quien se encarga de validar si se ha superado un highscore, quien luego actualiza el archivo `puntaje.txt` (implementado por las funciones `save_user_data` y `overwrite_users_list`, en `servidor/serpidor.py`)

##### ✅ Fin del Juego: La victoria y derrota del juego estan implementados en las funciones `game_over` y `game_finished`, ubicados en `cliente/backend/logica_utils/funciones_logica.py` y son utilizadas por la clase `LogicaInicio`

##### ✅ Recoger (G): Presionando esta tecla hace llamar a un metodo (`try_to_get_item`) donde, si el conejo esta encima de un item en el tablero, se podra recoger y añadir al inventario. Su implementacion se encuentra en `cliente/backend/logica_utils/funciones_logica` Ademas, me di la libertad de añadir a la letra (H) para poder *deseleccionar* el item. si es que uno se arrepiente de colocarlo en el tablero

##### ✅ Cheatcodes (Pausa, K+I+L, I+N+F): Los cheatcodes estan bien implementados y funcionan correctamente, al usar un cheatcode, este dura por toda la partida. Su implementacion se encuentra en `cliente/backend/logica_utils/funciones_logica`

##### ✅ Networking: Cada mensaje enviado entre el cliente y el servidor es codificado y encriptado antes de ser enviado. El server crea un *thread* por cada cliente, para poder manejar distintas instancias del juego a la vez. Cuando un thread asociado a un cliente necesita leer o sobreescribir el archivo `puntaje.txt`, primero adquiere el lock `user_list_lock()`, lee o escribe en el archivo, y luego lo suelta, con el objetivo de que el archivo sea leido/escrito por **un solo thread a la vez**

##### ✅ Decodificación: El mensaje se logra descodificar en base a la deteccion del numero de chunk y luego ir recibiendo el chunk mismo para ir armando el mensaje. La funcion encargada de realizar la decodificacion se encuentra en el metodo `listen_client_thread` de la clase `Servidor`

##### ✅ Desencriptación: El mensaje se logra desencriptar correctamente. La funcion encargada de realizar la descencriptacion es `decrypt(array: bytearray)`, ubicada en `servidor/files/funciones_servidor`

##### ✅ Archivos: Utilice todos los archivos entregados, a excepcion de los sonidos en `.mp3` (ya que uso los `.wav`), para `parametros.py` añadí algunos adicionales

##### ✅ Funciones: Utilice todas las funciones que creé durante la entrega intermedia, las asociadas a encriptacion y codificacion estan duplicadas para el cliente y el servidor. Algunas fueron modificadas ligeramente para adaptarlas a mi implementacion


## Ejecución :computer:
En base a lo que se menciono en la [issue #331](https://github.com/IIC2233/Syllabus/issues/331#issuecomment-1785883021), la forma de ejecutar la tarea es la siguente

El modulo principal **para el cliente** es `main.py` ubicado en `RUTA_A_LA_TAREA/entrega_final/cliente/`

```bash
python3 main.py <PORT>
```

El modulo principal **para el servidor** es `main.py` ubicado en `RUTA_A_LA_TAREA/entrega_final/servidor/`
```bash
python3 main.py <PORT>
```

Donde el `<PORT>` para el cliente y el servidor **deben ser el mismo**

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. `PyQt6`: `QtCore`, `QtGui`, `QtWidgets`, `QtMultimedia`
2. `sys`: `sys.exit`
3. `os`: `path.join`
4. `json`: `dumps`, `loads`, `load`
5. `threading`: `Thread`
6. `socket`
7. `typing`
8. `time`: `sleep`
9. `typing`: `Any`


### Librerías propias
A continuacion se muestran los modulos que cree para esta tarea. Las funciones que fueron creadas durante la entrega intermedia **estan indicadas con un \***, algunas de ellas fueron modificadas ligeramente respecto a la entrega intermedia

#### Cliente
##### Clases del Backend
1. `cliente.py`: Contiene a la clase `Cliente`. Posee metodos encargados de la comunicacion cliente-servidor y metodos encargados del intercambio de informacion entre el cliente y el backend logico

2. `logica_inicio.py`: Contiene a la clase `LogicaInicio`. Clase que hace de backend para la ventana de inicio, implementa la logica para el manejo de informacion al ingresar el nombre de usuario, manejar el envio de informacion del salón de la fama, etc

3. `logica_juego.py`: Contiene a la clase `LogicaJuego`. Clase que hace de backend para la ventana de juego, implementa la logica para el movimiento de las entidades y logica para el juego en si. Llego un punto en donde el archivo se me estaba haciendo muy largo, por lo que movi algunos metodos a la libreria `funciones_logica`

Librerias usadas por la clase `Cliente` y las clase `LogicaInicio` y `LogicaJuego`:

1. `cliente_utils`: contiene dos submodulos, utilizados por la clase `Cliente`
    - `funciones_cliente.py`: Contiene funciones asociadas a la **codificacion**, **encriptacion** (con funciones que creé en la *entrega intermedia*), ademas de funciones asociadas a la **decodificacion** y **desencriptacion** del mensaje:
        - `generador_secuencia` 
        - `serializar_mensaje`*
        - `separar_mensaje`*
        - `encriptar_mensaje`*
        - `codificar_mensaje`*
        - `quit_padding`
        - `which_is_different`
        - `decrypt`
        - `return_to_og_order`
        - `unscramble`
        - `split_array_even`
    
    - `mensaje.py`: Contiene a la clase `Mensaje`, necesaria para agilizar la comunicacion entre el cliente y el servidor 

2. `logica_utils`: Contiene nueve submodulos, utiliados por la clases `LogicaInicio` y `LogicaJuego`
    - `entity`: Contiene a la clase `Entity`. Clase que hereda de `QObject` y que actua como clase base para el jugador, los lobos y las zanahorias
    
    - `player`: Contiene a la clase `Player`. Objeto logico del jugador y que hereda de `Entity`, procesa los movimientos y las animaciones de una casilla a otra, ademas de gestionar sus propios sprites
    
    - `lobo`: Contiene a la clase `Lobo`. Objeto logico del lobo y que hereda de `Entity`, funciona de manera muy similar al jugador, con un animacion de movimiento y gestion de sprites propia
    
    - `zanahoria`: Contiene a la clase `Zanahoria`. Objeto logico de la zanahoria y que hereda de `Entity`

    - `canon`: Contiene a la clase `Canon`. Objeto logico de un cañon. Se encarga de crear zanahorias cada cierto tiempo

    - `item`: Contiene a las clase `Item`, de la cual heraden las clases `Manzana` y `Congelador`, tambien incluidas ahi. Son objetos que representan a los items que puede usar el jugador. `Item` es en realidad un `QThread` que se encarga de ir aplicando sus efectos en el tablero, dependiendo de que item es

    - `funciones_logica`: Contiene funciones utiles para el funcionamiento correcto del juego. Alguna son funciones que creé durante la *entrega intermedia*, y algunas son funciones para gestionar la posicion de entidades en el tablero y comprobar colisiones entre ellos. Ademas, aqui coloque algunos metodos de la clase `LogicaJuego` cuando el archivo se comenzó a alargar demasiado

        - `validacion_formato`*
        - `calcular_puntaje`*
        - `usar_item`*
        - `load_laberinto`
        - `duracion_nivel`
        - `velocidades_lobo`
        - `x_tab`
        - `y_tab`
        - `x_untab`
        - `y_untab`
        - `entities_overlapping`
        - `get_columna`
        - `separate_lists`
    
    - Ademas estan incluidas unas funciones que originalmente fueron metodos de `LogicaJuego`, pero que por temas de espacio, tuve que dejar acá:
        - `start_level_func`
        - `pausar_func`
        - `limpiar_datos_func`
        - `process_key_func`
        - `kil_shortcut`
        - `inf_shortcut`
        - `save_and_send`
        - `game_over`
        - `game_finished`

    - `funciones_jugador`: Contiene funciones utilizadas por `Player` y `Lobo`. La mayoria son funciones que creé durante la *entrega intermedia*, junto a funciones para poder iterar sobre el laberinto
        - `riesgo_mortal`*
        - `validar_direccion`*
        - `get_columna`
        - `in_between`
        - `generador_secuencia`

    - `parametros`: Contiene constantes utilizadas en el juego. Estan los obligatorios y algunos que coloque yo

##### Clases del Frontend
1. `ventana_de_inicio.py`: Frontend de la ventana de inicio implementado en la clase `VentanaInicio`

2. `ventana_de_juego.py`: Frontend de la ventana de juego implementado en la clase `VentanaJuego`

3. `labels.py`: Contiene a las clases `MovableLabel` (para entidades que se muevan, por ejemplo el jugador, los lobos, las zanahorias), `ImmovableLabel` (para entidades que no se mueven, como los cañones, el suelo y las paredes) e `ItemLabel` (para items colocados en la barra de inventario grafica) 

4. `pixmaps.py`: Crea un diccionario con los `QPixmaps` de las imagenes, para ir accediendo a ellos mas facilmente a traves de las *keys* del diccionario

5. `sounds.py`: Crea un diccionario con los `QUrl` de los sonidos en `.wav`, para poder ir accediendo a ellos mas facilmenrte a traves de las *keys*

6. `parametros_frontend.py`: Parametros utilizados por ambas ventanas. Contiene dimensiones, *fonts*, y los *paths* relativos a distintas imagenes y sonidos

#### Servidor
1. `servidor.py`: Contiene a la clase `Servidor`. Programa que se encarga de manejar las solicitudes de clientes que se puedan conectar, cada cliente es manejado por un `Thread`.

2. `utils`: Contiene modulos para un correcto funcionamiento del servidor
    - `funciones_servidor.py`: Contiene casi las mismas funciones que `funciones_cliente`. Son funciones encargadas de la **codificacion**, **encriptacion** (con funciones que creé en la *entrega intermedia*), ademas de funciones asociadas a la **decodificacion** y **desencriptacion** del mensaje
        - `usuario_permitido`*
        - `generador_secuencia` 
        - `serializar_mensaje`*
        - `separar_mensaje`*
        - `encriptar_mensaje`*
        - `codificar_mensaje`*
        - `quit_padding`
        - `which_is_different`
        - `decrypt`
        - `return_to_og_order`
        - `unscramble`
        - `split_array_even`

    - `mensaje.py`: Contiene a la misma clase `Mensaje`, necesaria para agilizar la comunicacion entre el cliente y el servidor

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:
1. ***SOBRE LA DESCONEXION DEL SERVIDOR***: El servidor se puede cerrar presionando cualquier tecla en la terminal (para probar la desconexion del servidor), cerrando el servidor de esta manera enviara automaticamente un mensaje a todos los clientes conectados. Si el servidor se cierra a la fuerza (con `ctrl-c` o cerrando su terminal), se notifica a los clientes conectados *justo despues de terminar un nivel*, ya que es en ese momento el cual se genera un intercambio de informacion entre el cliente y el server.


2. ***SOBRE EL MANEJO DE NIVELES***: Para los jugadores que hayan completado el juego, iniciarán desde el nivel 1, pero manteniendo su puntaje, de manera que este se va acumulando a medida que se van completando niveles. Mencionado en la [issue #345](https://github.com/IIC2233/Syllabus/issues/345#issuecomment-1792784907)

2. ***SOBRE LA FORMA DE COMUNICACION ENTRE EL CLIENTE Y EL SERVIDOR***: Luego de completar el proceso de desencriptacion y decodificacion, acabamos con un un *string* de la forma `{orden};{contenido}`, donde `orden` es un *string* y `contenido` puede ser cualquier objeto que puede ser serializado en `json`, contiene la informacion adicional asociada a la orden enviada. Este string luego es transformado a una lista con `split(";")` y se desempaquetan los datos en una clase Mensaje. El cliente y el servidor contienen una funcion (`handle_msg`) que es la que se encarga de ejecutar distintas funciones usando el `contenido` de la respuesta que le llegó, en funcion de la `orden` recibida. A continuacion unos ejemplos

    - Cliente a Servidor
        - `verify;<username>`
        - `disconnect;True`
        - `save;<datos_de_guardado>`


    - Servidor a Cliente
        - `top5;<lista>`
        - `verify;result`
        - `connection lost;<no contenido>`

3. ***SOBRE EL INVENTARIO***: Cuando el conejo muera, su inventario se reinicia, no obstante, los *items* ya recogidos vuelven a aparecer en el mapa, asi evitamos que exista un estado donde el jugador no tenga ninguna manera de poder eliminar a algun lobo

4. ***SOBRE LOS SHORTCUTS***: Los *shortcuts* `K+I+L` y `I+N+F` se activan correctamente solo si se presionan las teclas correctas una por una. Presionarlas todas al mismo tiempo, no asegura que se ejecute bien el *cheat*. Ademas ambos *cheats* duran **toda la sesion de juego** (los 3 niveles) una vez que fueron activados

5. ***SOBRE EL CALCULO DE LA VELOCIDAD*** (ALERTA MUCHO TEXTO): En mi implementacion, cuando una entidad se mueve de una casilla a otra, ademas de actualizar la *posicion interna* (actualizar un diccionario de posiciones, que representan los indices en la lista de listas de tablero), se ejecuta un `QTimer` en cargado de realizar la animacion de movimiendo de una casilla a otra, *sumando de a 1 pixel* , y actualizando la *posicion grafica*. Para poder alcanzar las velocidades especificadas en el enunciado realice lo siguente:
    - Poniendo de ejemplo al jugador, tenemos que debe moverse a $V = 10 \frac{casilla}{sec}$ (segun el enunciado y segun esta issue)

    - Para setear el intervalo de tiempo del `QTimer`, realice los siguentes calculos:

    - Como la velocidad es $V = 10 \frac{casilla}{sec}$, entonces el tiempo de movimiento es $t = \frac{1}{10}\frac{sec}{casilla}$

    - Como el timer va sumando 1 pixel cada iteracion (hasta llegar a la siguente casilla, luego se detiene), debemos entrar a considerar el tamaño del conejo, en mi caso todos los tamaños de mis imagenes son el mismo e igual a $T = 32\frac{pixel}{casilla}$ (lo deje especificado como constante en `parametros.py`)

    - Para obtener el valor que debe ir en el `QTimer`, multiplicamos ambos valores. $T_{QTimer} = t * T^{-1}$ y tenemos $\frac{1}{10}\frac{sec}{casilla}* \frac{1}{32}\frac{casilla}{pixel}$
    
    - Se cancela $casilla$ y terminamos con tiempo de intervalo debiese ser $T_{QTimer} = t * T^{-1} = \frac{1}{320}\frac{sec}{pixel}$ 
    
    - Luego, `setInterval` de `QTimer` solo recibe valores en $msec$ por lo que multiplicamos el valor anterior por el ponderador para cambiar de unidad ($1000 \frac{msec}{sec}$) y quedamos con $T_{QTimer} = \frac{1000}{320}\frac{msec}{pixel}$

    - Este calculo es el mismo aplicado para los lobos y las zanahorias, en el caso de la adicion de los ponderadores (para el cambio de nivel o para cuando una entidad esta congelada) simplemente se actualiza el valor de $T_{QTimer}$, dividiendolo por el valor del ponderador ($T_{QTimer} *  x_{ponderador}^{-1}$), que vendria siendo lo mismo que ponderar a la velocidad $V$

    - Una version este calculo fue confirmado en la [issue #342](https://github.com/IIC2233/Syllabus/issues/342). Ademas, hay que considerar que `setInterval` solo recibe valores *enteros*, por lo que me vi obligado a redondear el resultado final de $T_{QTimer}$.

6. ***SOBRE LOS EFECTOS DE LAS BOMBAS*** En base a lo que se menciono en la [issue #355](https://github.com/IIC2233/Syllabus/issues/355#issuecomment-1792822606), las bombas manzana son capaces de: eliminar a todos los lobos a su alcance, pero ademas destruyen cañones, matan al jugador e eliminan items en el tablero. La bomba congeladora afecta a los lobos, pero tambien afecta al jugador, reduciendo su velocidad en un 25%, la bomba congeladora no afecta a los cañones. Pregunte acerca de si esto era valido de hacer en la [issue #378](https://github.com/IIC2233/Syllabus/issues/378)

8. ***SOBRE LA FRECUENCIA DE DISPAROS DE ZANAHORIAS***: La frecuencia de disparo de los cañones es de **3 segundos** (esta indicado en `parametros.py`)

9. Como lo indique en la parte de la pauta me di la libertad de añadir a la letra (H) para poder *deseleccionar* el item. si es que uno se arrepiente de colcoar un item.

10. Por mas que trate de definir la posicion en la que aparecen las ventanas, estas aparecen en una posicion random. Estuve buscando en internet e incluso lo pregunte en la [issue #143](https://github.com/IIC2233/Syllabus/issues/143) hace algunas semanas, pero sigo sin tener solucion. Al parecer es una *feature* de WSL. Aun asi, deje definido que las ventanas de generaran en la **esquina superior izquierda** de la pantalla. Ejecutando el programa desde *Windows* se podrá notar.
-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. [PyQt6 Dialogs and Alerts](https://www.pythonguis.com/tutorials/pyqt6-dialogs/). Es un mini-tutorial para implementar ventanas *pop-up* usando la clase `QMessageBox`. Esta implementado en los archivos:
    - `cliente/frontend/ventana_de_inicio.py` en la linea 123 y 206. 
    - `cliente/frontend/ventana_de_juego.py` en la linea 193 y 214

2. [Determine if two rectangles overlap each other?](https://stackoverflow.com/questions/306316/determine-if-two-rectangles-overlap-each-other). Codigo para saber para si un rectangulo esta encima de otro, o viceversa. Lo use para implementar el gestor de colisiones del juego. Esta presente en el archivo `cliente/backend/logica_utils/funciones_logica.py` en la funcion `entities_overlapping()` en las lineas 69 a 90. Tambien use [esta pagina](https://silentmatt.com/rectangle-intersection/) para poder visualizar mejor como funcionaabn las colisiones entre entidades

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).