from fastapi import APIRouter, status
from api.v1.offers import views

router = APIRouter(prefix='/auth')
router.add_api_route(
    "/offers/",
    endpoint=views.get_all_offers_view,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    description="Get all offers view.",
    tags=["Offers"]
)
router.add_api_route(
    "/offers/{offer_id}",
    endpoint=views.get_offer_by_id_view,
    methods=["GET"],
    status_code=status.HTTP_200_OK,
    description="Get offer view.",
    tags=["Offers"]
)
router.add_api_route(
    "/offers/{offer_id}",
    endpoint=views.update_offer_view,
    methods=["PUT"],
    status_code=status.HTTP_200_OK,
    description="Update offer view.",
    tags=["Offers"]
)
router.add_api_route(
    "/offers/",
    endpoint=views.create_offer_view,
    methods=["POST"],
    status_code=status.HTTP_201_CREATED,
    description="Create an offer view.",
    tags=["Offers"]
)
