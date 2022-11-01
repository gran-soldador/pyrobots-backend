from fastapi import APIRouter, HTTPException, status, Response
import engine
from engine.outputmodels import SimulationResult
from cattrs.preconf.json import make_converter
# TODO: Do other cattrs preconfs


converter = make_converter()
router = APIRouter()


@router.get("/simulacion", response_model=SimulationResult)
async def estado_juego():
    try:
        result = engine.run_demo_game()
        # We COULD do `return result`, but some quick measurements show that
        # is ~10 times slower.
        json_str = converter.dumps(result)
        return Response(json_str, media_type="application/json")
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) from e
