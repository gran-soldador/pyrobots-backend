from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from endpoints import helloworld, listar_partidas

app = FastAPI()
app.include_router(helloworld.router)
app.include_router(listar_partidas.router)

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET'],
    allow_headers=['Content-Type', 'application/xml'],
)
