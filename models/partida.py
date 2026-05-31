from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

#cambios
class PartidaBase(SQLModel):
    jugador1_id: int = Field(..., description="ID del primer jugador")
    jugador2_id: int = Field(..., description="ID del segundo jugador")
    ganador_id: int = Field(..., description="ID del jugador ganador")
    fecha: date = Field(..., description="Fecha de la partida")


class PartidaID(PartidaBase, table=True):
    __tablename__ = "partidas"
    id: Optional[int] = Field(default=None, primary_key=True)


class PartidaUpdate(SQLModel):
    jugador1_id: Optional[int] = Field(default=None)
    jugador2_id: Optional[int] = Field(default=None)
    ganador_id: Optional[int] = Field(default=None)
    fecha: Optional[date] = Field(default=None)


class RankingID(SQLModel, table=True):
    __tablename__ = "rankings"
    id: Optional[int] = Field(default=None, primary_key=True)
    jugador_id: int = Field(..., foreign_key="jugadores.id")
    nombre: str = Field(...)
    puntos: int = Field(default=0)
    posicion: int = Field(...)