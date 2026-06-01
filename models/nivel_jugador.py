from enum import Enum
from sqlmodel import SQLModel, Field
from typing import Optional

class NivelJugador(str, Enum):
    principiante = "principiante"
    intermedio   = "intermedio"
    profesional  = "profesional"

class Categoria(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str