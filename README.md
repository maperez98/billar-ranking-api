<div align="center">
<br/>

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

<br/>

**Sistema web para gestión y clasificación de jugadores de billar**  
*Proyecto Integrador — Desarrollo de Software*

<br/>

[🌐 **Demo en Vivo**](https://billar-ranking-api.onrender.com) • [📦 **Repositorio**](https://github.com/maperez98/billar-ranking-api)

</div>

## 📄 Documentación

[📥 Ver Informe Técnico](docs/informe_tecnico_billar-ranking.pdf)
---

## 🎯 Objetivo

Aplicación web construida con **FastAPI** que permite:

- Gestionar jugadores de billar con foto de perfil
- Registrar y validar partidas
- Calcular un **ranking automático** con criterios de desempate
- Visualizar estadísticas en un **dashboard interactivo**

---

## ✨ Funcionalidades

| Feature | Estado |
|---|:---:|
| CRUD completo de jugadores con foto | ✅ |
| Registro de partidas con validaciones | ✅ |
| Ranking automático con desempate | ✅ |
| Dashboard con 4 gráficas interactivas | ✅ |
| Búsqueda por nombre y país | ✅ |
| Validaciones en frontend y backend | ✅ |
| Fotos en Supabase Storage | ✅ |
| Base de datos PostgreSQL en Neon | ✅ |
| Deploy con CI/CD automático en Render | ✅ |

---

## 🛠️ Stack Tecnológico

<div align="center">

| Categoría | Tecnología | Uso |
|---|---|---|
| **Backend** | FastAPI | Framework principal |
| **ORM** | SQLModel | Modelos de base de datos |
| **Base de datos** | Neon (PostgreSQL) | Almacenamiento remoto en la nube |
| **Storage** | Supabase Storage | Fotos de jugadores |
| **Deploy** | Render | Hosting con CI/CD |
| **Frontend** | Bulma CSS + Jinja2 | Estilos y plantillas HTML |
| **Gráficas** | Chart.js | Visualización de estadísticas |
| **Lenguaje** | Python 3.12 | — |

</div>

---

## 📁 Estructura del Proyecto

```
billar-ranking-api/
│
├── models/
│   ├── jugador.py          ← Modelo de jugadores
│   ├── partida.py          ← Modelo de partidas y ranking
│   └── nivel_jugador.py    ← Enum de niveles
│
├── operations/
│   ├── operations_jugador.py   ← CRUD jugadores
│   └── operations_partida.py  ← CRUD partidas y ranking
│
├── templates/              ← HTML con Jinja2 + Bulma
├── static/                 ← Archivos estáticos
├── db.py                   ← Conexión a Neon
├── supabase_client.py      ← Conexión a Supabase
├── main.py                 ← Rutas API y HTML
└── requirements.txt
```

---

## 🗄️ Modelos de Datos

<details>
<summary><b>👤 Jugador</b></summary>

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `int` | Identificador único |
| `nombre` | `str` | Nombre del jugador (2–50 chars) |
| `edad` | `int` | Edad (18–100) |
| `pais` | `str` | País de origen |
| `nivel` | `enum` | `principiante` / `intermedio` / `profesional` |
| `activo` | `bool` | Estado del jugador |
| `foto_url` | `str` | URL de foto en Supabase |

</details>

<details>
<summary><b>🎮 Partida</b></summary>

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `int` | Identificador único |
| `jugador1_id` | `int` | ID del primer jugador |
| `jugador2_id` | `int` | ID del segundo jugador |
| `ganador_id` | `int` | ID del jugador ganador |
| `fecha` | `date` | Fecha de la partida |

</details>

<details>
<summary><b>🏆 Ranking</b></summary>

| Campo | Tipo | Descripción |
|---|---|---|
| `id` | `int` | Identificador único |
| `jugador_id` | `int` | Referencia al jugador |
| `nombre` | `str` | Nombre del jugador |
| `puntos` | `int` | Puntos acumulados (10 por victoria) |
| `posicion` | `int` | Posición en el ranking |
| `partidas_jugadas` | `int` | Total de partidas jugadas |

</details>

---

## 🔗 Endpoints

<details>
<summary><b>🖥️ Páginas HTML</b></summary>

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/` | Página principal con ranking |
| `GET` | `/jugadores-pagina` | Lista de jugadores |
| `GET` | `/partidas-pagina` | Lista de partidas |
| `GET` | `/jugadores/nuevo` | Formulario nuevo jugador |
| `GET` | `/partidas/nuevo` | Formulario nueva partida |
| `GET` | `/dashboard` | Dashboard con estadísticas |
| `GET` | `/buscar?q=nombre` | Búsqueda de jugadores |

</details>

<details>
<summary><b>👤 API Jugadores</b></summary>

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/jugadores` | Listar jugadores activos |
| `POST` | `/jugadores` | Crear jugador (JSON) |
| `POST` | `/jugadores/con-foto` | Crear jugador con foto |
| `GET` | `/jugadores/{id}` | Obtener jugador por ID |
| `PATCH` | `/jugadores/{id}` | Actualizar jugador |
| `DELETE` | `/jugadores/{id}` | Desactivar jugador |
| `GET` | `/jugadores/buscar/nombre?nombre=x` | Buscar por nombre |
| `GET` | `/jugadores/buscar/pais?pais=x` | Buscar por país |
| `GET` | `/jugadores/filtrar?atributo=x&valor=y` | Filtrar jugadores |

</details>

<details>
<summary><b>🎮 API Partidas</b></summary>

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/partidas` | Listar todas las partidas |
| `POST` | `/partidas` | Registrar nueva partida |
| `PATCH` | `/partidas/{id}` | Actualizar partida |
| `DELETE` | `/partidas/{id}` | Eliminar partida |

</details>

<details>
<summary><b>🏆 API Ranking</b></summary>

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/ranking` | Ver ranking actual |
| `POST` | `/ranking/calcular` | Recalcular ranking |
| `GET` | `/ranking/top/{limite}` | Top N jugadores |

</details>

---

## ⚙️ Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL_NEON=postgresql://usuario:password@host/neondb?sslmode=require
SUPABASE_URL=https://tuproyecto.supabase.co
SUPABASE_KEY=tu_clave_publica
```

---

## 🚀 Instalación y Ejecución Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/maperez98/billar-ranking-api.git
cd billar-ranking-api

# 2. Crear entorno virtual
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# (crear archivo .env con las variables indicadas arriba)

# 5. Correr el servidor
uvicorn main:app --reload
```

Abre [`http://localhost:8000`](http://localhost:8000) en tu navegador.  
La documentación interactiva estará disponible en [`http://localhost:8000/docs`](http://localhost:8000/docs).

---

## 👤 Autor

<div align="center">

**Miguel Angel Perez Vargas**  
*Proyecto Integrador — Desarrollo de Software*

[![GitHub](https://img.shields.io/badge/GitHub-maperez98-181717?style=for-the-badge&logo=github)](https://github.com/maperez98)

</div>
