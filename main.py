from fastapi import FastAPI
from models import Jugador
from operations import crear_jugador, obtener_jugadores

app = FastAPI()

@app.post("/Crear_jugadores")
def crear(jugador: Jugador):
    return crear_jugador(jugador)



@app.get("/Lista_jugadores")
def listar():
    return obtener_jugadores()
