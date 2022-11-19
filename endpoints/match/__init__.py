from fastapi import APIRouter

from . import exit_match
from . import join_match
from . import list_matches
from . import lobby
from . import new_match
from . import show_match_results
from . import start_match

router = APIRouter()

router.include_router(exit_match.router)
router.include_router(join_match.router)
router.include_router(list_matches.router)
router.include_router(lobby.router)
router.include_router(new_match.router)
router.include_router(show_match_results.router)
router.include_router(start_match.router)
