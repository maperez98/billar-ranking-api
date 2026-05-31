from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from fastapi import HTTPException
from models.jugador import JugadorBase, JugadorID, JugadorUpdate


def crear_jugador(jugador: JugadorBase, session: Session):
    nuevo = JugadorID.model_validate(jugador)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


def obtener_jugadores(session: Session, solo_activos: bool = True):
    query = select(JugadorID)
    if solo_activos:
        query = query.where(JugadorID.activo == True)
    return session.exec(query).all()


def obtener_jugador_por_id(id: int, session: Session):
    try:
        return session.get_one(JugadorID, id)
    except NoResultFound:
        return None


def actualizar_jugador(id: int, datos: JugadorUpdate, session: Session):
    jugador = obtener_jugador_por_id(id, session)
    if jugador is None:
        raise HTTPException(status_code=404, detail=f"Jugador {id} no encontrado")
    update_data = datos.model_dump(exclude_unset=True)
    jugador.sqlmodel_update(update_data)
    session.add(jugador)
    session.commit()
    session.refresh(jugador)
    return jugador


def eliminar_jugador(id: int, session: Session):
    jugador = obtener_jugador_por_id(id, session)
    if jugador is None:
        raise HTTPException(status_code=404, detail=f"Jugador {id} no encontrado")
    if not jugador.activo:
        raise HTTPException(status_code=400, detail="El jugador ya está inactivo")
    jugador.activo = False
    session.add(jugador)
    session.commit()
    return {"mensaje": "jugador desactivado", "id": id}


def buscar_por_nombre(nombre: str, session: Session):
    query = select(JugadorID).where(
        JugadorID.nombre.ilike(f"%{nombre}%"),
        JugadorID.activo == True
    )
    return session.exec(query).all()


def buscar_por_pais(pais: str, session: Session):
    query = select(JugadorID).where(
        JugadorID.pais.ilike(pais),
        JugadorID.activo == True
    )
    return session.exec(query).all()


def filtrar_jugadores(atributo: str, valor: str, session: Session):
    atributos_validos = ["pais", "nivel", "nombre"]
    if atributo not in atributos_validos:
        raise HTTPException(
            status_code=400,
            detail=f"Atributo no válido. Usa: {atributos_validos}"
        )
    query = select(JugadorID).where(JugadorID.activo == True)
    if atributo == "pais":
        query = query.where(JugadorID.pais.ilike(valor))
    elif atributo == "nivel":
        query = query.where(JugadorID.nivel.ilike(valor))
    elif atributo == "nombre":
        query = query.where(JugadorID.nombre.ilike(f"%{valor}%"))
    return session.exec(query).all()