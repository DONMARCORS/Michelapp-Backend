import logging

from fastapi import APIRouter, Body, Depends, HTTPException

from app import crud
from app.api import deps
from app.schemas.product import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductSearchResults
)
from app.models.user import User

router = APIRouter()

logger = logging.getLogger(__name__)

@router.get("/all-products", status_code=200, response_model=ProductSearchResults)
def get_all_products() -> dict:
    """
    Get all products, used by admin and vendedor
    """
    return {"results": list()}

