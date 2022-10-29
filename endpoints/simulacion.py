from fastapi import APIRouter, HTTPException, status
import engine
from engine.outputmodels import SimulationResult


router = APIRouter()


@router.get("/simulacion", response_model=SimulationResult)
async def estado_juego():
    try:
        return engine.run_demo_game()
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) from e
