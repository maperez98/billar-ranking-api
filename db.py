import os
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, SQLModel
from fastapi import FastAPI, Depends
from typing import Annotated
from contextlib import asynccontextmanager

load_dotenv()

neon_db = os.getenv("DATABASE_URL_NEON")


engine = create_engine(neon_db, echo=True)

@asynccontextmanager
async def create_all_tables(app: FastAPI):
    print("⏳ Intentando conectar y asegurar tablas en Neon...")
    SQLModel.metadata.create_all(engine)
    print("Tablas listas y sincronizadas")
    yield
def get_session() -> Session:
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]