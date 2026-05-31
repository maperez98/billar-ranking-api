from sqlmodel import SQLModel, Field
from models.nivel_jugador import NivelJugador
from typing import Optional


class JugadorBase(SQLModel):
    nombre : str          = Field(..., min_length=2, max_length=50)
    edad   : int          = Field(..., ge=18, le=100)
    pais   : str          = Field(..., min_length=2, max_length=50)
    nivel  : NivelJugador = Field(...)
    activo : bool         = Field(default=True)


class JugadorID(JugadorBase, table=True):
    __tablename__ = "jugadores"
    id: Optional[int] = Field(default=None, primary_key=True)


class JugadorUpdate(SQLModel):
    nombre : Optional[str]          = Field(default=None, min_length=2, max_length=50)
    edad   : Optional[int]          = Field(default=None, ge=18, le=100)
    pais   : Optional[str]          = Field(default=None, min_length=2, max_length=50)
    nivel  : Optional[NivelJugador] = Field(default=None)
    activo : Optional[bool]         = Field(default=None)