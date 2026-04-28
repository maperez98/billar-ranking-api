import csv
from models import Jugador, Partida

FILE_JUGADORES = "jugadores.csv"
FILE_PARTIDAS = "partidas.csv"
FILE_RANKING = "rankings.csv"

#     MODELO JUGADORES CRUD

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
            writer.writerow(["id", "nombre", "edad", "pais", "nivel", "activo"])

        writer.writerow([
            jugador.id,
            jugador.nombre,
            jugador.edad,
            jugador.pais,
            jugador.nivel.value if hasattr(jugador.nivel, 'value') else jugador.nivel,
            jugador.activo
        ])

    return {"mensaje": "jugador creado", "id": jugador.id}


def obtener_jugadores(solo_activos=True):
    jugadores = []

    try:
        with open(FILE_JUGADORES, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) >= 6:
                    jugador = {
                        "id": int(row[0]),
                        "nombre": row[1],
                        "edad": int(row[2]),
                        "pais": row[3],
                        "nivel": row[4],
                        "activo": row[5].lower() == 'true' if len(row) > 5 else True
                    }
                    if solo_activos and not jugador["activo"]:
                        continue
                    jugadores.append(jugador)
                elif len(row) == 5:
                    jugador = {
                        "id": int(row[0]),
                        "nombre": row[1],
                        "edad": int(row[2]),
                        "pais": row[3],
                        "nivel": row[4],
                        "activo": True
                    }
                    if solo_activos:
                        jugadores.append(jugador)
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
    jugadores = obtener_jugadores(solo_activos=False)
    actualizado = False

    for j in jugadores:
        if j["id"] == id and j["activo"]:
            j["activo"] = False
            actualizado = True
            break

    if actualizado:
        with open(FILE_JUGADORES, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "nombre", "edad", "pais", "nivel", "activo"])

            for j in jugadores:
                writer.writerow([
                    j["id"],
                    j["nombre"],
                    j["edad"],
                    j["pais"],
                    j["nivel"],
                    j["activo"]
                ])
        return {"mensaje": "jugador desactivado ", "id": id}
    else:
        return {"mensaje": "jugador no encontrado o ya inactivo", "id": id}


#     MODELO PARTIDAS:

def crear_partida(partida: Partida):
    jugadores = obtener_jugadores()
    jugadores_ids = [j["id"] for j in jugadores]

    if partida.jugador1_id not in jugadores_ids:
        return {"error": f"Jugador {partida.jugador1_id} no existe", "id": partida.id}
    if partida.jugador2_id not in jugadores_ids:
        return {"error": f"Jugador {partida.jugador2_id} no existe", "id": partida.id}
    if partida.ganador_id not in jugadores_ids:
        return {"error": f"Jugador {partida.ganador_id} no existe", "id": partida.id}

    if partida.jugador1_id == partida.jugador2_id:
        return {"error": "El jugador no puede jugar consigo mismo", "id": partida.id}

    if partida.ganador_id not in [partida.jugador1_id, partida.jugador2_id]:
        return {"error": "El ganador debe ser uno de los dos jugadores", "id": partida.id}

    archivo_existe = False
    try:
        with open(FILE_PARTIDAS, mode="r"):
            archivo_existe = True
    except FileNotFoundError:
        pass

    with open(FILE_PARTIDAS, mode="a", newline="") as file:
        writer = csv.writer(file)

        if not archivo_existe:
            writer.writerow(["id", "jugador1_id", "jugador2_id", "ganador_id", "fecha"])

        writer.writerow([
            partida.id,
            partida.jugador1_id,
            partida.jugador2_id,
            partida.ganador_id,
            partida.fecha
        ])

    return {"mensaje": "partida creada", "id": partida.id}


def obtener_partidas():
    partidas = []

    try:
        with open(FILE_PARTIDAS, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) == 5:
                    partidas.append({
                        "id": int(row[0]),
                        "jugador1_id": int(row[1]),
                        "jugador2_id": int(row[2]),
                        "ganador_id": int(row[3]),
                        "fecha": row[4]
                    })
    except FileNotFoundError:
        return []
    except StopIteration:
        return []

    return partidas


def actualizar_partida(id: int, datos: dict):
    partidas = obtener_partidas()
    actualizado = False

    for p in partidas:
        if p["id"] == id:
            p["jugador1_id"] = datos.get("jugador1_id", p["jugador1_id"])
            p["jugador2_id"] = datos.get("jugador2_id", p["jugador2_id"])
            p["ganador_id"] = datos.get("ganador_id", p["ganador_id"])
            p["fecha"] = datos.get("fecha", p["fecha"])
            actualizado = True
            break

    if actualizado:
        with open(FILE_PARTIDAS, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "jugador1_id", "jugador2_id", "ganador_id", "fecha"])

            for p in partidas:
                writer.writerow([
                    p["id"],
                    p["jugador1_id"],
                    p["jugador2_id"],
                    p["ganador_id"],
                    p["fecha"]
                ])
        return {"mensaje": "partida actualizada", "id": id}
    else:
        return {"mensaje": "partida no encontrada", "id": id}


def eliminar_partida(id: int):
    partidas = obtener_partidas()
    nuevas = [p for p in partidas if p["id"] != id]

    eliminado = len(nuevas) != len(partidas)

    if eliminado:
        with open(FILE_PARTIDAS, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["id", "jugador1_id", "jugador2_id", "ganador_id", "fecha"])

            for p in nuevas:
                writer.writerow([
                    p["id"],
                    p["jugador1_id"],
                    p["jugador2_id"],
                    p["ganador_id"],
                    p["fecha"]
                ])
        return {"mensaje": "partida eliminada", "id": id}
    else:
        return {"mensaje": "partida no encontrada", "id": id}

#         MODELO RANKING : READ RANKING ES LOQ UE INTERESA, PORQUE  ESTAMOS HACIENDO CALCULOS

def calcular_ranking():
    partidas = obtener_partidas()
    jugadores = obtener_jugadores()

    puntos = {}
    for j in jugadores:
        puntos[j["id"]] = 0

    for p in partidas:
        puntos[p["ganador_id"]] = puntos.get(p["ganador_id"], 0) + 10

    ranking_ordenado = sorted(puntos.items(), key=lambda x: x[1], reverse=True)

    with open(FILE_RANKING, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["posicion", "jugador_id", "puntos", "nombre"])

        for posicion, (jugador_id, puntaje) in enumerate(ranking_ordenado, 1):
            nombre = "Desconocido"
            for j in jugadores:
                if j["id"] == jugador_id:
                    nombre = j["nombre"]
                    break

            writer.writerow([posicion, jugador_id, puntaje, nombre])

    return {"mensaje": "ranking calculado y guardado"}


def obtener_ranking():
    ranking = []

    try:
        with open(FILE_RANKING, mode="r") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                if len(row) == 4:
                    ranking.append({
                        "posicion": int(row[0]),
                        "jugador_id": int(row[1]),
                        "puntos": int(row[2]),
                        "nombre": row[3]
                    })
    except FileNotFoundError:
        return []
    except StopIteration:
        return []

    return ranking


def obtener_top_jugadores(limite=5):
    ranking = obtener_ranking()
    return ranking[:limite]