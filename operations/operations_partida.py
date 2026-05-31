from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from fastapi import HTTPException
from models.partida import PartidaBase, PartidaID, PartidaUpdate, RankingID
from models.jugador import JugadorID


def crear_partida(partida: PartidaBase, session: Session):
    ids_activos = [j.id for j in session.exec(
        select(JugadorID).where(JugadorID.activo == True)
    ).all()]

    if partida.jugador1_id not in ids_activos:
        raise HTTPException(status_code=404, detail=f"Jugador {partida.jugador1_id} no existe o está inactivo")
    if partida.jugador2_id not in ids_activos:
        raise HTTPException(status_code=404, detail=f"Jugador {partida.jugador2_id} no existe o está inactivo")
    if partida.ganador_id not in ids_activos:
        raise HTTPException(status_code=404, detail=f"Jugador {partida.ganador_id} no existe o está inactivo")
    if partida.jugador1_id == partida.jugador2_id:
        raise HTTPException(status_code=400, detail="Un jugador no puede jugar contra sí mismo")
    if partida.ganador_id not in [partida.jugador1_id, partida.jugador2_id]:
        raise HTTPException(status_code=400, detail="El ganador debe ser uno de los dos jugadores")

    nueva = PartidaID.model_validate(partida)
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


def obtener_partidas(session: Session):
    return session.exec(select(PartidaID)).all()


def actualizar_partida(id: int, datos: PartidaUpdate, session: Session):
    try:
        partida = session.get_one(PartidaID, id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    update_data = datos.model_dump(exclude_unset=True)
    partida.sqlmodel_update(update_data)
    session.add(partida)
    session.commit()
    session.refresh(partida)
    return partida


def eliminar_partida(id: int, session: Session):
    try:
        partida = session.get_one(PartidaID, id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
    session.delete(partida)
    session.commit()
    return {"mensaje": "partida eliminada", "id": id}


def calcular_ranking(session: Session):
    for r in session.exec(select(RankingID)).all():
        session.delete(r)
    session.commit()

    jugadores = session.exec(
        select(JugadorID).where(JugadorID.activo == True)
    ).all()
    puntos  = {j.id: 0       for j in jugadores}
    nombres = {j.id: j.nombre for j in jugadores}

    for partida in session.exec(select(PartidaID)).all():
        if partida.ganador_id in puntos:
            puntos[partida.ganador_id] += 10

    for posicion, (jugador_id, puntaje) in enumerate(
        sorted(puntos.items(), key=lambda x: x[1], reverse=True), start=1
    ):
        session.add(RankingID(
            jugador_id=jugador_id,
            nombre=nombres.get(jugador_id, "Desconocido"),
            puntos=puntaje,
            posicion=posicion
        ))
    session.commit()
    return {"mensaje": "ranking calculado y guardado"}


def obtener_ranking(session: Session):
    return session.exec(select(RankingID).order_by(RankingID.posicion)).all()


def obtener_top_jugadores(limite: int, session: Session):
    return session.exec(
        select(RankingID).order_by(RankingID.posicion).limit(limite)
    ).all()