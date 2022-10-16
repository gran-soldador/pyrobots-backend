from fastapi import APIRouter, status, HTTPException
from engine import run_demo_game

router = APIRouter()


@router.get("/simulacion")
async def estado_juego(status_code=status.HTTP_200_OK):
    try:
        return run_demo_game()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='error en la simulación')
