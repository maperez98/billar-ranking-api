from sqlmodel import SQLModel, Field
from typing import Optional

class JugadorBase(SQLModel):
    nombre: str
    edad: int
    pais: str
    nivel: str
    activo: bool = True


class JugadorID(JugadorBase, table=True):
    __tablename__ = "jugadores"
    id: Optional[int] = Field(default=None, primary_key=True)


class JugadorUpdate(SQLModel):
    nombre: Optional[str] = None
    edad: Optional[int] = None
    pais: Optional[str] = None
    nivel: Optional[str] = None
    activo: Optional[bool] = None