from fastapi import APIRouter

from . import change_robot_code
from . import get_robot_code
from . import list_robots
from . import new_robot

router = APIRouter()

router.include_router(change_robot_code.router)
router.include_router(get_robot_code.router)
router.include_router(list_robots.router)
router.include_router(new_robot.router)
