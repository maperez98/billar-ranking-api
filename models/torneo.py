from sqlmodel import SQLModel, Field
from typing import Optional

class Torneo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    categoria_id: int = Field(foreign_key="categoria.id")