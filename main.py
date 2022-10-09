from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from endpoints import helloworld

app = FastAPI()
app.include_router(helloworld.router)

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
