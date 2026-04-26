from pydantic import BaseModel, Field
from datetime import date
from nivel_Jugador import NivelJugador

class Jugador(BaseModel):
    id: int = Field(..., description="Id del jugador")
    nombre: str = Field(..., min_length=2, max_length=50)
    edad: int = Field(..., ge=18, le=100)
    pais: str = Field(..., min_length=2, max_length=50)
    nivel: NivelJugador


class Partida(BaseModel):
    id: int = Field(..., description="Id de la partida")
    jugador1_id: int = Field(..., description="ID del primer jugador")
    jugador2_id: int = Field(..., description="ID del segundo jugador")
    ganador_id: int = Field(..., description="ID del jugador ganador")
    fecha: date = Field(..., description="Fecha de la partida")



class Ranking(BaseModel):
    jugador_id: int = Field(..., description="ID del jugador")
    puntos: int = Field(0, ge=0)
    posicion: int = Field(..., ge=1)

