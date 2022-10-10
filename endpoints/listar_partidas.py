from fastapi import APIRouter
from db import *

router = APIRouter()


@router.get("/lista_partidas")
async def listar_partidas():
    return Persona.select().to_json()
