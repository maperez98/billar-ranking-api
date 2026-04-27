from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_jugador():
    response = client.post("/jugadores", json={
        "id": 10,
        "nombre": "Jugador Test",
        "edad": 25,
        "pais": "Colombia",
        "nivel": "principiante"
    })
    assert response.status_code == 200
    assert response.json()["mensaje"] == "jugador creado"
    assert response.json()["id"] == 10


def test_obtener_jugadores():
    response = client.get("/jugadores")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_actualizar_jugador():
    response = client.put("/jugadores/10", json={
        "nombre": "Jugador Modificado",
        "edad": 30
    })
    assert response.status_code == 200
    assert response.json()["mensaje"] == "jugador actualizado"


def test_eliminar_jugador():
    response = client.delete("/jugadores/10")
    assert response.status_code == 200
    assert response.json()["mensaje"] == "jugador eliminado"


def test_crear_partida():
    response = client.post("/partidas", json={
        "id": 10,
        "jugador1_id": 1,
        "jugador2_id": 2,
        "ganador_id": 1,
        "fecha": "2024-04-27"
    })
    assert response.status_code == 201
    assert response.json()["mensaje"] == "partida creada"


def test_obtener_partidas():
    response = client.get("/partidas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_actualizar_partida():
    response = client.put("/partidas/10", json={
        "ganador_id": 2
    })
    assert response.status_code == 200
    assert response.json()["mensaje"] == "partida actualizada"


def test_eliminar_partida():
    response = client.delete("/partidas/10")
    assert response.status_code == 200
    assert response.json()["mensaje"] == "partida eliminada"


def test_calcular_ranking():
    response = client.post("/ranking/calcular")
    assert response.status_code == 200
    assert response.json()["mensaje"] == "ranking calculado y guardado"


def test_obtener_ranking():
    response = client.get("/ranking")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_top_jugadores():
    response = client.get("/ranking/top/3")
    assert response.status_code == 200
    assert isinstance(response.json(), list)