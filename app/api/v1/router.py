from fastapi import APIRouter
from api.v1.auth.router import router as auth_router
from api.v1.offers.router import router as offers_router
from api.v1.websocket.router import router as websocket_router

router = APIRouter(prefix='/v1')
router.include_router(auth_router)
router.include_router(offers_router)
router.include_router(websocket_router)
