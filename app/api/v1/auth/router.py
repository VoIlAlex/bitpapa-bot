from fastapi import APIRouter, status
from api.v1.auth import views

router = APIRouter(prefix='/auth')
router.add_api_route(
    "/token/",
    endpoint=views.token_view,
    methods=["POST"],
    status_code=status.HTTP_200_OK,
    description="Retrieve a JWT token.",
    tags=["Auth"]
)
router.add_api_route(
    "/token/refresh/",
    endpoint=views.refresh_view,
    methods=["POST"],
    status_code=status.HTTP_200_OK,
    description="Refresh JWT token.",
    tags=["Auth"]
)
router.add_api_route(
    "/me/",
    endpoint=views.me_view,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    description="Get current user.",
    tags=["Auth"]
)
