from fastapi import APIRouter, status, HTTPException
import engine
# from engine import run_demo_game

router = APIRouter()


@router.get("/simulacion")
async def estado_juego():
    try:
        return engine.run_demo_game()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='error en la simulación')
