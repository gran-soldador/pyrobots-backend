from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from endpoints import (registrar_usuario, endpoint_login, listar_robot,
                       crear_robot, verify_user, crear_partida, simulacion,
                       listar_partidas, unir_partida, abandonar_partida,
                       mostrar_resultados, lobby, iniciar_partida,
                       enviar_mail_recuperacion_contrasena,
                       recuperar_contrasena)

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
app.include_router(unir_partida.router)
app.include_router(abandonar_partida.router)
app.include_router(mostrar_resultados.router)
app.include_router(lobby.router)
app.include_router(iniciar_partida.router)
app.include_router(enviar_mail_recuperacion_contrasena.router)
app.include_router(recuperar_contrasena.router)

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
