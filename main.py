from fastapi import FastAPI, status
from models import Jugador, Partida
from operations_csv import crear_jugador, obtener_jugadores, actualizar_jugador, eliminar_jugador
from operations_csv import crear_partida, actualizar_partida, eliminar_partida, obtener_partidas
from operations_csv import obtener_ranking, obtener_top_jugadores, calcular_ranking
app = FastAPI(title="Billar Ranking API")

@app.post("/jugadores")
def crear_nuevo_jugador(jugador: Jugador):
    return crear_jugador(jugador)

@app.get("/jugadores")
def listar_jugadores():
    return obtener_jugadores()

@app.put("/jugadores/{jugador_id}")
def actualizar_jugador_endpoint(jugador_id: int, jugador: dict):
    return actualizar_jugador(jugador_id, jugador)

@app.delete("/jugadores/{jugador_id}")
def eliminar_jugador_endpoint(jugador_id: int):
    return eliminar_jugador(jugador_id)

@app.post("/partidas", status_code=status.HTTP_201_CREATED)
def crear_nueva_partida(partida: Partida):
    return crear_partida(partida)

@app.get("/partidas")
def listar_partidas():
    return obtener_partidas()

@app.put("/partidas/{partida_id}")
def actualizar_partida_endpoint(partida_id: int, datos: dict):
    return actualizar_partida(partida_id, datos)

@app.delete("/partidas/{partida_id}")
def eliminar_partida_endpoint(partida_id: int):
    return eliminar_partida(partida_id)

@app.get("/ranking")
def ver_ranking():
    return obtener_ranking()

@app.post("/ranking/calcular")
def calcular_nuevo_ranking():
    return calcular_ranking()

@app.get("/ranking/top/{limite}")
def ver_top_jugadores(limite: int = 5):
    return obtener_top_jugadores(limite)