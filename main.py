from fastapi import FastAPI, HTTPException, status
from models import Jugador
from operations import crear_jugador, obtener_jugadores, actualizar_jugador, eliminar_jugador

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