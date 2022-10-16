from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from endpoints import helloworld, registrar_usuario, endpoint_login


app = FastAPI()

app.include_router(helloworld.router)
app.include_router(registrar_usuario.router)
app.include_router(endpoint_login.auth_routes)

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
