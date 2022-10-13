from fastapi import APIRouter, status, HTTPException
from engine.demo import demo

router = APIRouter()


@router.get("/simulacion")
async def estado_juego():
    try:
        return demo()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='error en la simulación')
