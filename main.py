from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from endpoints import helloworld, simulacion

app = FastAPI()
app.include_router(helloworld.router)
app.include_router(simulacion.router)

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
