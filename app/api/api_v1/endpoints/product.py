import logging

from fastapi import APIRouter

from app.schemas.product import (
    ProductSearchResults
)

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/all-products", status_code=200, response_model=ProductSearchResults)
def get_all_products() -> dict:
    """
    Get all products, used by admin and vendedor
    """
    return {"results": list()}

