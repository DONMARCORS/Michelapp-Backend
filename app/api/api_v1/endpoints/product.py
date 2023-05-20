import logging

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app import crud
from app.api import deps

from app.models.user import User
from app.schemas.product import ProductUpdate



from app.schemas.product import (
    ProductSearchResults
)

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/all", status_code=200, response_model=ProductSearchResults)
def get_all_products() -> dict:
    """
    Get all products, used by admin and vendedor
    """
    return {"results": list()}


