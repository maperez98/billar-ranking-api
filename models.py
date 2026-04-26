from pydantic import BaseModel, Field
from datetime import date
from nivel_Jugador import NivelJugador



class Jugador(BaseModel):
    id: int = Field(..., description="Identificador único del jugador")
    nombre: str = Field(..., min_length=2, max_length=50)
    edad: int = Field(..., ge=10, le=100)
    pais: str = Field(..., min_length=2, max_length=50)
    nivel: NivelJugador


# 🎱 MODELO: Partida
class Partida(BaseModel):
    id: int = Field(..., description="Identificador único de la partida")
    jugador1_id: int = Field(..., description="ID del primer jugador")
    jugador2_id: int = Field(..., description="ID del segundo jugador")
    ganador_id: int = Field(..., description="ID del jugador ganador")
    fecha: date = Field(..., description="Fecha de la partida")


# 🏆 MODELO: Ranking
class Ranking(BaseModel):
    jugador_id: int = Field(..., description="ID del jugador")
    puntos: int = Field(0, ge=0)
    posicion: int = Field(..., ge=1)