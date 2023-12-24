from backend.logica_inicio import LogicaInicio
from backend.logica_juego import LogicaJuego
from backend.cliente import Cliente
from frontend.ventana_de_inicio import VentanaInicio
from frontend.ventana_de_juego import VentanaJuego
from PyQt6.QtWidgets import QApplication
from backend.logica_utils import parametros as p
import sys
from os.path import join
from json import load

"""
Archivo principal a correr para el cliente

"""

if __name__ == "__main__":
    # crear un cliente, pasarle como argumentos el backend y el frontend
    PORT = None
    HOST = None

    try:
        if len(sys.argv) >= 2:
            PORT = int(sys.argv[1])

            with open(join(*(p.RUTA_HOST.split('/')))) as file:
                HOST = load(file)['host']

            app = QApplication([])

            # inicializacion de entidades
            # frontend
            v_inicio = VentanaInicio()
            v_juego = VentanaJuego()

            # backend
            logica_inicio = LogicaInicio()
            logica_juego = LogicaJuego()
            cliente = Cliente(PORT, HOST, logica_inicio, logica_juego)

            # Conexion de señales
            # 1. ventana de inicio -> backend inicio
            v_inicio.senal_validar_nombre.connect(logica_inicio.validar_nombre)
            v_inicio.senal_salir_ventana_inicio.connect(
                logica_inicio.salir_ventana_inicio)

            # 2. backend inicio -> ventana de inicio
            logica_inicio.senal_iniciar_ventana_inicio.connect(
                v_inicio.iniciar_ventana_inicio)
            logica_inicio.senal_anadir_jugador_data.connect(
                v_inicio.anadir_jugador_data)
            logica_inicio.senal_mostrar_popup.connect(v_inicio.mostrar_popup)
            logica_inicio.senal_cerrar_ventana_por_desconexion.connect(
                v_inicio.salir)
            logica_inicio.senal_ocultar_inicio.connect(v_inicio.ocultar_inicio)

            # 3. backend inicio -> cliente
            logica_inicio.senal_on_front_close.connect(cliente.on_front_close)
            logica_inicio.senal_enviar_data_al_server.connect(
                cliente.send_data_to_server)

            # 4. cliente -> backend inicio
            cliente.senal_cerrar_ventana_por_desconexion.connect(
                logica_inicio.cerrar_ventana_por_desconexion)
            cliente.senal_enviar_jugador_data.connect(
                logica_inicio.anadir_jugador_data)
            cliente.senal_enviar_player_status.connect(
                logica_inicio.set_player_status)

            # 5. backend inicio <-> backend juego
            logica_inicio.senal_iniciar_juego.connect(
                logica_juego.start_simulation)
            logica_inicio.senal_send_game_data.connect(
                logica_juego.load_game_data)

            # 6. ventana de juego -> backend juego
            v_juego.senal_salir_ventana_juego.connect(
                logica_juego.salir_ventana_juego)
            v_juego.senal_key_press.connect(logica_juego.procesar_key_press)
            v_juego.senal_pausar.connect(logica_juego.pausar)
            v_juego.senal_pos.connect(logica_juego.procesar_posicion_clickeada)
            v_juego.senal_selected_item.connect(
                logica_juego.procesar_item_seleccionado)

            # 7. backend juego -> ventana de juego
            logica_juego.senal_start_simulation.connect(
                v_juego.start_simulation)
            # logica_inicio.senal_cerrar_ventana_por_desconexion.connect(
            #     v_juego.salir)
            logica_juego.senal_place_tile.connect(v_juego.place_tile)
            logica_juego.senal_set_title.connect(v_juego.set_title)
            logica_juego.senal_cambio_segundos.connect(
                v_juego.cambiar_segundos)
            logica_juego.senal_mensaje_pop_up.connect(v_juego.mostrar_popup)

            # estas señales puede que cambien
            logica_juego.senal_spawn_player.connect(v_juego.player.spawn_label)
            logica_juego.senal_move_player.connect(v_juego.player.move_label)
            logica_juego.senal_raise_player_label.connect(
                v_juego.player.raise_label)

            # senales de creacion y borrado de labels movibles
            logica_juego.senal_create_entity_label.connect(
                v_juego.create_movable_label)
            logica_juego.senal_delete_entities.connect(
                v_juego.delete_current_labels)
            logica_juego.senal_kill_entity_label.connect(v_juego.kill_entity)

            # senales de manejo de labels movibles
            logica_juego.senal_spawn_entity.connect(v_juego.spawn_entity)
            logica_juego.senal_move_entity.connect(v_juego.move_entity)
            logica_juego.senal_send_music.connect(v_juego.play_sound)
            logica_juego.senal_juego_terminado_pop_up.connect(
                v_juego.juego_terminado)

            logica_juego.senal_place_item_inventory.connect(
                v_juego.place_item_inventory)
            logica_juego.senal_deactivate_item_label.connect(
                v_juego.item_usado)

            # 8. backend_juego -> cliente
            logica_juego.senal_on_front_close.connect(cliente.on_front_close)
            logica_juego.senal_enviar_data_al_server.connect(
                cliente.send_data_to_server)

            # 9. cliente -> backend juego
            cliente.senal_cerrar_ventana_por_desconexion.connect(
                logica_juego.cerrar_ventana_por_desconexion)

            # inicio app
            cliente.logica_inicio.start_inicio()

            # --- ejecucion de la app ---

            app.exec()

            print("> main.py: Usuario cerrado correctamente")

        else:
            print("> Error. No se detecto un puerto ingresado")

    except ValueError:
        print('> Error. Ingresa un puerto valido')
