from fastapi import APIRouter
from app.api import users, alerts, auth, fall_detection

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(fall_detection.router, prefix="/fall-detection", tags=["fall-detection"])