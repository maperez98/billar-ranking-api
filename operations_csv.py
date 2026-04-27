import csv
from models import Jugador

FILE_JUGADORES = "jugadores.csv"


def crear_jugador(jugador: Jugador):
    archivo_existe = False
    try:
        with open(FILE_JUGADORES, mode="r"):
            archivo_existe = True
    except FileNotFoundError:
        pass

    with open(FILE_JUGADORES, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not archivo_existe:
            writer.writerow(["id", "nombre", "edad", "pais", "nivel"])

        writer.writerow([
            jugador.id,
            jugador.nombre,
            jugador.edad,
            jugador.pais,
            jugador.nivel.value if hasattr(jugador.nivel, 'value') else jugador.nivel
        ])

    return {"mensaje": "jugador creado", "id": jugador.id}


def obtener_jugadores():
    jugadores = []

    try:
        with open(FILE_JUGADORES, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) == 5:
                    jugadores.append({
                        "id": int(row[0]),
                        "nombre": row[1],
                        "edad": int(row[2]),
                        "pais": row[3],
                        "nivel": row[4]
                    })
    except FileNotFoundError:
        return []
    except StopIteration:
        return []

    return jugadores


def actualizar_jugador(id: int, datos: dict):
    jugadores = obtener_jugadores()
    actualizado = False

    for j in jugadores:
        if j["id"] == id:
            j["nombre"] = datos.get("nombre", j["nombre"])
            j["edad"] = datos.get("edad", j["edad"])
            j["pais"] = datos.get("pais", j["pais"])
            j["nivel"] = datos.get("nivel", j["nivel"])
            actualizado = True
            break

    if actualizado:

        with open(FILE_JUGADORES, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "nombre", "edad", "pais", "nivel"])

            for j in jugadores:
                writer.writerow([
                    j["id"],
                    j["nombre"],
                    j["edad"],
                    j["pais"],
                    j["nivel"]
                ])
        return {"mensaje": "jugador actualizado", "id": id}
    else:
        return {"mensaje": "jugador no encontrado", "id": id}


def eliminar_jugador(id: int):
    jugadores = obtener_jugadores()
    nuevos = [j for j in jugadores if j["id"] != id]

    eliminado = len(nuevos) != len(jugadores)

    if eliminado:
        with open(FILE_JUGADORES, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "nombre", "edad", "pais", "nivel"])

            for j in nuevos:
                writer.writerow([
                    j["id"],
                    j["nombre"],
                    j["edad"],
                    j["pais"],
                    j["nivel"]
                ])
        return {"mensaje": "jugador eliminado", "id": id}
    else:
        return {"mensaje": "jugador no encontrado", "id": id}