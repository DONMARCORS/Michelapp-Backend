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
def get_all_products(
    *,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Get all products, used by admin and vendedor
    """

    results = crud.product.get_multi(db=db)
    if not results:
        return {"results": []}

    return {"results": results}

#Este endpoint es para editar un producto, recibe un id y un objeto de tipo ProductUpdate
@router.put("/{product_id}", status_code=200, response_model=ProductUpdate)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> dict:
    """
    Update a product
    """
    if current_user.privilege == "admin":
        return {"product": product}
