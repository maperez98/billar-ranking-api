import csv
from models import Jugador
from models import Partida

FILE_JUGADORES = "jugadores.csv"


def crear_jugador(jugador: Jugador):
    try:
        with open(FILE_JUGADORES, mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "nombre", "edad", "pais", "nivel"])
    except FileExistsError:
        pass

    with open(FILE_JUGADORES, mode="a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            jugador.id,
            jugador.nombre,
            jugador.edad,
            jugador.pais,
            jugador.nivel
        ])

    return {"mensaje": "jugador creado"}


def obtener_jugadores():
    jugadores = []

    try:
        with open(FILE_JUGADORES, mode="r") as file:
            reader = csv.reader(file)

            for row in reader:
                jugadores.append({
                    "id": row[0],
                    "nombre": row[1],
                    "edad": row[2],
                    "pais": row[3],
                    "nivel": row[4]
                })

    except FileNotFoundError:
        return []

    return jugadores