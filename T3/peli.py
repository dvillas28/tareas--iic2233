import api
import requests


class Peliculas:

    def __init__(self, host, port):
        self.base = f"http://{host}:{port}"

    def saludar(self) -> dict:
        response = requests.get(f'{self.base}/')
        json = response.json()
        status = response.status_code
        return {"status-code": status, "saludo": json["result"]}

    def verificar_informacion(self, pelicula: str) -> bool:
        response = requests.get(f'{self.base}/peliculas')
        peliculas = response.json()["result"]

        if pelicula in peliculas:
            return True
        return False

    def dar_informacion(self, pelicula: str) -> dict:
        response = requests.get(
            f'{self.base}/informacion', params={"pelicula": pelicula})
        info = response.json()["result"]
        status = response.status_code
        return {"status-code": status, "mensaje": info}

    def dar_informacion_aleatoria(self) -> dict:
        response = requests.get(f'{self.base}/aleatorio')
        link = response.json()["result"]
        status = response.status_code

        if status == 200:
            response = requests.get(link)
            status = response.status_code
            info = response.json()["result"]
            return {"status-code": status, "mensaje": info}

        else:
            return {"status-code": status, "mensaje": link}

    def agregar_informacion(self, pelicula: str, sinopsis: str, access_token: str) -> dict:
        header = {"Authorization": access_token}
        data = {"pelicula": pelicula, "sinopsis": sinopsis}
        response = requests.post(
            f'{self.base}/update', headers=header, data=data)

        status = response.status_code

        if status == 401:
            return "Agregar pelicula no autorizado"
        elif status == 400:
            return response.json()["result"]
        return "La base de la API ha sido actualizada"

    def actualizar_informacion(self, pelicula: str, sinopsis: str, access_token: str) -> dict:
        header = {"Authorization": access_token}
        data = {"pelicula": pelicula, "sinopsis": sinopsis}

        response = requests.patch(
            f'{self.base}/update', headers=header, data=data)

        status = response.status_code

        if status == 401:
            return "Editar información no autorizado"
        elif status == 200:
            return "La base de la API ha sido actualizada"
        return response.json()["result"]

    def eliminar_pelicula(self, pelicula: str, access_token: str) -> dict:
        header = {"Authorization": access_token}
        data = {"pelicula": pelicula}

        response = requests.delete(
            f'{self.base}/remove', headers=header, data=data)

        status = response.status_code

        if status == 401:
            return "Eliminar pelicula no autorizado"
        elif status == 200:
            return "La base de la API ha sido actualizada"
        return response.json()["result"]


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 4444
    DATABASE = {
        "Mamma Mia": "Mamma Mia es una Comedia musical con ABBA",
        "Monsters Inc": "Monsters Inc trata sobre monstruos que asustan, niños y risas",
        "Incredibles": "Incredibles trata de una familia de superhéroes que salva el mundo",
        "Avengers": "Avengers trata de superhéroes que luchan contra villanos poderosos",
        "Titanic": "Titanic es sobre amor trágico en el hundimiento del Titanic",
        "Akira": "Akira es una película de ciencia ficción japonesa con poderes psíquicos",
        "High School Musical": "High School Musical es un drama musical adolescente en East High",
        "The Princess Diaries": "The Princess Diaries es sobre Mia, una joven que descubre que es"
        "princesa de Genovia",
        "Iron Man": "Iron Man trata sobre un hombre construye traje de alta tecnología "
        "para salvar al mundo",
        "Tarzan": "Tarzan es sobre un hombre criado por simios en la jungla",
        "The Pianist": "The Pianist es sobre un músico judío que sobrevive en Varsovia"
        " durante el Holocausto",
    }
    thread = api.Server(HOST, PORT, DATABASE)
    thread.start()

    Peliculas = Peliculas(HOST, PORT)
    print(Peliculas.saludar())
    print(Peliculas.dar_informacion_aleatoria())
    print(Peliculas.actualizar_informacion("Titanic", "Titanic es sobre amor trágico inspitado"
                                           " en el historico hundimiento del Titanic", "tereiic2233"))
    print(Peliculas.verificar_informacion("Tarzan"))
    print(Peliculas.dar_informacion("The Princess Diaries"))
    print(Peliculas.dar_informacion("Monsters Inc"))
    print(Peliculas.agregar_informacion("Matilda", "Matilda es sobre una niña con poderes"
                                        "telequinéticos que enfrenta a su malvada directora",
                                        "tereiic2233"))
    print(Peliculas.dar_informacion("Matilda"))
