from fastapi import FastAPI, HTTPException, Request, Depends, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session
from fastapi.responses import RedirectResponse

from db import SessionDep, create_all_tables, get_session
from models.jugador import JugadorBase, JugadorID, JugadorUpdate
from models.partida import PartidaBase, PartidaID, PartidaUpdate, RankingID


from operations.operations_jugador import (
    crear_jugador, obtener_jugadores, obtener_jugador_por_id,
    actualizar_jugador, eliminar_jugador,
    buscar_por_nombre, buscar_por_pais, filtrar_jugadores,subir_foto_a_storage
)
from operations.operations_partida import (
    crear_partida, obtener_partidas, actualizar_partida, eliminar_partida,
    calcular_ranking, obtener_ranking, obtener_top_jugadores,
)

app = FastAPI(title="Billar Ranking API 🎱", lifespan=create_all_tables)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/", response_class=HTMLResponse)
async def home(request: Request, session: Session = Depends(get_session)):
    ranking = obtener_ranking(session)
    return templates.TemplateResponse(request, "ranking.html", {"ranking": ranking})

@app.get("/jugadores-pagina", response_class=HTMLResponse)
async def pagina_jugadores(request: Request, session: Session = Depends(get_session)):
    jugadores = obtener_jugadores(session, solo_activos=False)
    return templates.TemplateResponse(request, "jugadores.html", {"jugadores": jugadores})

@app.get("/partidas-pagina", response_class=HTMLResponse)
async def pagina_partidas(request: Request, session: Session = Depends(get_session)):
    partidas  = obtener_partidas(session)
    jugadores = obtener_jugadores(session, solo_activos=False)
    return templates.TemplateResponse(request, "partidas.html", {
        "partidas": partidas, "jugadores": jugadores
    })



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

@app.get("/jugadores/nuevo", response_class=HTMLResponse)
async def pagina_registro(request: Request):
    return templates.TemplateResponse(request, "registro_jugador.html", {})

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



@app.post("/partidas", response_model=PartidaID)
def api_crear_partida(partida: PartidaBase, session: SessionDep):
    return crear_partida(partida, session)

@app.get("/partidas", response_model=list[PartidaID])
def api_listar_partidas(session: SessionDep):
    return obtener_partidas(session)

@app.patch("/partidas/{id}", response_model=PartidaID)
def api_actualizar_partida(id: int, datos: PartidaUpdate, session: SessionDep):
    return actualizar_partida(id, datos, session)

@app.delete("/partidas/{id}")
def api_eliminar_partida(id: int, session: SessionDep):
    return eliminar_partida(id, session)



@app.get("/ranking", response_model=list[RankingID])
def api_ranking(session: SessionDep):
    return obtener_ranking(session)

@app.post("/ranking/calcular")
def api_calcular_ranking(session: SessionDep):
    return calcular_ranking(session)

@app.get("/ranking/top/{limite}", response_model=list[RankingID])
def api_top(limite: int, session: SessionDep):
    return obtener_top_jugadores(limite, session)


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


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    print(f"Error detectado: {exc}")

    return templates.TemplateResponse("error.html", {
        "request": request,
        "mensaje": "Ha ocurrido un error inesperado. Por favor, intenta de nuevo."
    })


