from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from sys import version_info, stderr

from endpoints import router

if not version_info >= (3, 10):  # pragma: no cover
    print("Python 3.10 or higher is required to run PyRobots\n", file=stderr)
    exit(1)

load_dotenv()  # Important for loading .env file with JWT SECRET

app = FastAPI()
app.include_router(router)

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
