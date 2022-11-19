from fastapi import APIRouter

from . import change_password
from . import change_user_avatar
from . import login
from . import profile
from . import recover_password
from . import register
from . import request_recovery
from . import verify_user

router = APIRouter()

router.include_router(change_password.router)
router.include_router(change_user_avatar.router)
router.include_router(login.router)
router.include_router(profile.router)
router.include_router(recover_password.router)
router.include_router(register.router)
router.include_router(request_recovery.router)
router.include_router(verify_user.router)
