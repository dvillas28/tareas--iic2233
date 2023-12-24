import sys
from os.path import join
from json import load
from servidor import Servidor
from utils.parametros_servidor import RUTA_HOST

if __name__ == "__main__":
    try:
        if len(sys.argv) >= 2:
            PORT = sys.argv[1]

            with open(join(*(RUTA_HOST.split('/')))) as file:
                HOST = load(file)['host']

            server = Servidor(PORT, HOST)
            input("\nPRESIONA ENTER EN CUALQUIER MOMENTO PARA CERRAR EL SERVIDOR\n")

            print('> Cerrando Servidor. Notificando a clientes conectados')
            server.desconectar_sockets()

        else:
            print("> Puerto no indicado. Ingresa un puerto")
    except ValueError:
        print("> Error. Ingresa un puerto valido")
