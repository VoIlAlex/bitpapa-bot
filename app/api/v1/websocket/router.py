from fastapi import APIRouter, status
from api.v1.websocket import views

router = APIRouter()
router.add_websocket_route(
    "/api/v1/offers/{offer_id}/websocket/",
    endpoint=views.websocket_endpoint
)
router.add_websocket_route(
    "/api/v1/websocket/ping/",
    endpoint=views.websocket_ping
)

