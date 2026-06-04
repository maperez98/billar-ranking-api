from fastapi import FastAPI, HTTPException, Request, Depends, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from datetime import datetime
from collections import Counter

from db import SessionDep, create_all_tables, get_session
from models.jugador import JugadorBase, JugadorID, JugadorUpdate
from models.partida import PartidaBase, PartidaID, PartidaUpdate, RankingID

from operations.operations_jugador import (
    crear_jugador, obtener_jugadores, obtener_jugador_por_id,
    actualizar_jugador, eliminar_jugador,
    buscar_por_nombre, buscar_por_pais, filtrar_jugadores, subir_foto_a_storage
)
from operations.operations_partida import (
    crear_partida, obtener_partidas, actualizar_partida, eliminar_partida,
    calcular_ranking, obtener_ranking, obtener_top_jugadores,
)

app = FastAPI(title="Billar Ranking API", lifespan=create_all_tables)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


#EStos son los endpoints para pagina HTML

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session: Session = Depends(get_session)):
    ranking = obtener_ranking(session)
    return templates.TemplateResponse(request, "ranking.html", {
        "ranking": ranking, "active": "ranking"
    })

@app.get("/jugadores-pagina", response_class=HTMLResponse)
async def pagina_jugadores(request: Request, session: Session = Depends(get_session)):
    jugadores = obtener_jugadores(session, solo_activos=False)
    return templates.TemplateResponse(request, "jugadores.html", {
        "jugadores": jugadores, "active": "jugadores"
    })

@app.get("/partidas-pagina", response_class=HTMLResponse)
async def pagina_partidas_v2(request: Request, session: Session = Depends(get_session)):
    partidas  = obtener_partidas(session)
    jugadores = obtener_jugadores(session, solo_activos=False)
    nombres   = {j.id: j.nombre for j in jugadores}
    return templates.TemplateResponse(request, "partidas.html", {
        "partidas": partidas, "jugadores": jugadores,
        "nombres": nombres, "active": "partidas"
    })

@app.get("/jugadores/nuevo", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(request, "registro_jugador.html", {})

@app.get("/partidas/nuevo", response_class=HTMLResponse)
async def pagina_nueva_partida(request: Request, session: Session = Depends(get_session)):
    jugadores = obtener_jugadores(session)
    return templates.TemplateResponse(request, "registro_partida.html", {"jugadores": jugadores})

@app.post("/ranking/calcular-html", response_class=HTMLResponse)
async def calcular_ranking_html(request: Request, session: Session = Depends(get_session)):
    calcular_ranking(session)
    ranking = obtener_ranking(session)
    return templates.TemplateResponse(request, "ranking.html", {
        "ranking": ranking, "active": "ranking",
        "mensaje": "Ranking recalculado correctamente"
    })

@app.get("/buscar", response_class=HTMLResponse)
async def buscar_html(
    request: Request,
    q: str = "",
    tipo: str = "nombre",
    session: Session = Depends(get_session)
):
    resultados = []
    if q:
        if tipo == "pais":
            resultados = buscar_por_pais(q, session)
        else:
            resultados = buscar_por_nombre(q, session)
    return templates.TemplateResponse(request, "buscar.html", {
        "resultados": resultados, "query": q, "tipo": tipo
    })

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, session: Session = Depends(get_session)):
    jugadores = obtener_jugadores(session, solo_activos=True)
    partidas  = obtener_partidas(session)
    ranking   = obtener_ranking(session)
    nombres   = {j.id: j.nombre for j in jugadores}

    nivel_counter    = Counter(j.nivel for j in jugadores)
    pais_counter     = Counter(j.pais  for j in jugadores)
    victoria_counter = Counter(p.ganador_id for p in partidas)

    return templates.TemplateResponse(request, "dashboard.html", {
        "active":          "dashboard",
        "total_jugadores": len(jugadores),
        "total_partidas":  len(partidas),
        "lider":           ranking[0].nombre if ranking else "-",
        "total_paises":    len(pais_counter),
        "ranking_nombres": [r.nombre for r in ranking],
        "ranking_puntos":  [r.puntos  for r in ranking],
        "nivel_labels":    list(nivel_counter.keys()),
        "nivel_counts":    list(nivel_counter.values()),
        "victoria_names":  [nombres.get(k, str(k)) for k in victoria_counter],
        "victoria_counts": list(victoria_counter.values()),
        "pais_labels":     list(pais_counter.keys()),
        "pais_counts":     list(pais_counter.values()),
    })


# Api de los jugadors

@app.post("/jugadores", response_model=JugadorID)
def api_crear_jugador(jugador: JugadorBase, session: SessionDep):
    return crear_jugador(jugador, session)

@app.get("/jugadores", response_model=list[JugadorID])
def api_listar_jugadores(session: SessionDep):
    return obtener_jugadores(session)

@app.get("/jugadores/inactivos", response_model=list[JugadorID])
def api_inactivos(session: SessionDep):
    return obtener_jugadores(session, solo_activos=False)

@app.get("/jugadores/filtrar", response_model=list[JugadorID])
def api_filtrar(atributo: str, valor: str, session: SessionDep):
    return filtrar_jugadores(atributo, valor, session)

@app.get("/jugadores/buscar/nombre", response_model=list[JugadorID])
def api_buscar_nombre(nombre: str, session: SessionDep):
    return buscar_por_nombre(nombre, session)

@app.get("/jugadores/buscar/pais", response_model=list[JugadorID])
def api_buscar_pais(pais: str, session: SessionDep):
    return buscar_por_pais(pais, session)

@app.get("/jugadores/{id}", response_model=JugadorID)
def api_obtener_jugador(id: int, session: SessionDep):
    jugador = obtener_jugador_por_id(id, session)
    if not jugador:
        raise HTTPException(status_code=404, detail=f"Jugador {id} no encontrado")
    return jugador

@app.patch("/jugadores/{id}", response_model=JugadorID)
def api_actualizar_jugador(id: int, datos: JugadorUpdate, session: SessionDep):
    return actualizar_jugador(id, datos, session)

@app.delete("/jugadores/{id}")
def api_eliminar_jugador(id: int, session: SessionDep):
    return eliminar_jugador(id, session)

@app.post("/jugadores/con-foto")
async def api_crear_jugador_con_foto(
        request: Request,
        nombre: str = Form(...),
        edad: int = Form(...),
        pais: str = Form(...),
        nivel: str = Form(...),
        foto: UploadFile = File(...),
        session: Session = Depends(get_session)
):
    try:
        contenido = await foto.read()
        url_foto = subir_foto_a_storage(contenido, foto.filename)
        datos_jugador = JugadorBase(nombre=nombre, edad=edad, pais=pais, nivel=nivel)
        crear_jugador(datos_jugador, session, url_foto=url_foto)
        return RedirectResponse(url="/jugadores-pagina", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": f"Error al registrar: {str(e)}"
        })


# API para las partidas

@app.post("/partidas")
async def api_crear_partida(
        request: Request,
        jugador1_id: int = Form(...),
        jugador2_id: int = Form(...),
        ganador_id: int = Form(...),
        fecha: str = Form(...),
        session: Session = Depends(get_session)
):
    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
        if ganador_id not in [jugador1_id, jugador2_id]:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "mensaje": "El ganador debe ser uno de los dos jugadores."
            })
        partida = PartidaBase(
            jugador1_id=jugador1_id,
            jugador2_id=jugador2_id,
            ganador_id=ganador_id,
            fecha=fecha_obj
        )
        crear_partida(partida, session)
        calcular_ranking(session)
        return RedirectResponse(url="/partidas-pagina", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "mensaje": f"Error tecnico: {str(e)}"
        })

@app.get("/partidas", response_model=list[PartidaID])
def api_listar_partidas(session: SessionDep):
    return obtener_partidas(session)

@app.patch("/partidas/{id}", response_model=PartidaID)
def api_actualizar_partida(id: int, datos: PartidaUpdate, session: SessionDep):
    return actualizar_partida(id, datos, session)

@app.delete("/partidas/{id}")
def api_eliminar_partida(id: int, session: SessionDep):
    return eliminar_partida(id, session)


# APIpara los ranking

@app.get("/ranking", response_model=list[RankingID])
def api_ranking(session: SessionDep):
    return obtener_ranking(session)

@app.post("/ranking/calcular")
def api_calcular_ranking(session: SessionDep):
    return calcular_ranking(session)

@app.get("/ranking/top/{limite}", response_model=list[RankingID])
def api_top(limite: int, session: SessionDep):
    return obtener_top_jugadores(limite, session)


# MAnjear los errorres (LAs excepciones)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Error detectado: {exc}")
    return templates.TemplateResponse("error.html", {
        "request": request,
        "mensaje": "Ha ocurrido un error inesperado. Por favor, intenta de nuevo."
    })