from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from endpoints import registrar_usuario, endpoint_login, listar_robot
from endpoints import crear_robot, verify_user
from dotenv import load_dotenv
from endpoints import crear_partida, simulacion, listar_partidas


app = FastAPI()

load_dotenv()  # Important for loading .env file with JWT SECRET

app.include_router(registrar_usuario.router)
app.include_router(endpoint_login.auth_routes)
app.include_router(crear_robot.router)
app.include_router(crear_partida.router)
app.include_router(listar_partidas.router)
app.include_router(listar_robot.router)
app.include_router(simulacion.router)
app.include_router(verify_user.router)

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
