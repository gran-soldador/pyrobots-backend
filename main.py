from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from endpoints import helloworld, registrar_usuario, endpoint_login
from dotenv import load_dotenv
from endpoints.endpoint_login import auth_routes


app = FastAPI()

load_dotenv()

app.include_router(helloworld.router)
app.include_router(registrar_usuario.router)
app.include_router(auth_routes)
app.include_router(endpoint_login.auth_routes)

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
