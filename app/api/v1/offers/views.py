from typing import List

from fastapi import Depends, HTTPException, status

from api.v1.offers.inputs import OfferInput
from api.v1.offers.outputs import OfferOutput
from db.models import Offer
from service.auth.login import JWTService


async def get_all_offers_view(
    _=Depends(JWTService.get_current_user)
) -> List[OfferOutput]:
    offers = await Offer.get_all()
    return offers


async def get_offer_by_id_view(
    offer_id: int,
    _=Depends(JWTService.get_current_user)
) -> OfferOutput:
    offer = await Offer.get_by_id(offer_id)
    if offer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found."
        )
    return offer


async def create_offer_view(
    data: OfferInput,
    _=Depends(JWTService.get_current_user)
) -> OfferOutput:
    offer = await Offer.create(**data.dict())
    return offer


async def update_offer_view(
    offer_id: int,
    data: OfferInput,
    _=Depends(JWTService.get_current_user)
) -> OfferOutput:
    offer = await Offer.get_by_id(offer_id)
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )

    await offer.update(**data.dict())
    return offer


async def delete_offer_view(
    offer_id: int,
    _=Depends(JWTService.get_current_user)
):
    offer = await Offer.get_by_id(offer_id)
    if not offer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Offer not found"
        )
    await offer.delete()
