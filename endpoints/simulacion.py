from fastapi import APIRouter, status, HTTPException, Depends, Form
from .functions_jwt import *
import engine


router = APIRouter()


@router.get("/simulacion")
async def estado_juego():
    try:
        return engine.run_demo_game()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='error en la simulación')

@router.post("/create_simulation")
async def simulation(user_id: int = Depends(authenticated_user),
                     id_robots: List[int] = Form(...)
                    ):
    try:
        g = engine.Game([]).simulation()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='error en la simulación')