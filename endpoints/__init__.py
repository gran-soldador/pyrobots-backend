from fastapi import APIRouter

from . import user
from . import robot
from . import match
from . import simulation

router = APIRouter()

router.include_router(user.router)
router.include_router(robot.router)
router.include_router(match.router)
router.include_router(simulation.router)
