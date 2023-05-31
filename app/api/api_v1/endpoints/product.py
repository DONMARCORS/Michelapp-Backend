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
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Get all products, used by admin and vendedor
    """

    results = crud.product.get_multi(db=db)
    if not results:
        return {"results": []}

    return {"results": results}


@router.put("/{product_id}", status_code=200, response_model=ProductUpdate)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Update a product
    """
    if current_user.privilege == "admin":
        return {"product": product}
    
    
#Caso de uso: Crear un producto nuevo en la base de datos
@router.post("/", status_code=201, response_model="Product Created")
def create_product(
    *,
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
        example={
        "product_id": 123,
        "name": "Clamato",
        "description": "Jugo de tomate preparado con almejas y especias.",
        "price": 32.5,
        "stock": 34,
        "image": "String",
        }
) -> dict:
    """
    Create a product. Only client cannot create products
    """
    if current_user.privilege != 3:
        return {"product": product}
    
    if current_user.privilege == "vendedor":
        raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found",
    if user_in.privilage != 1 and user_in.privilage != 2:
        raise HTTPException(status_code=403, detail="Not authorized to perform this action")

#Caso de uso: Eliminar un producto de la base de datos
@router.delete("/{product_id}", status_code=200, response_model=ProductUpdate)
def delete_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Delete a product. Only client cannot delete products
    """
    if current_user.privilege == "admin":
        return {"product": product}
    
    raise HTTPException(
        status_code=404,
        detail=f"Product {item.product_id} not found",
    )|