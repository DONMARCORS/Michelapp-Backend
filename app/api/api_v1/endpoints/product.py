import logging

from fastapi import APIRouter, Body, Depends, HTTPException

from sqlalchemy.orm import Session
from app import crud
from app.api import deps

from app.models.user import User
from app.schemas.product import ProductUpdate, ProductCreate, Product



from app.schemas.product import (
    ProductSearchResults
)

router = APIRouter()

logger = logging.getLogger(__name__)

authorization_exception = HTTPException(
        status_code=403,
        detail="Not authorized to perform this action",
    )


#Caso de uso: Obtener todos los productos de la base de datos
@router.get("/", status_code=200, response_model=ProductSearchResults)
def get_products(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Get all products
    """
    results = crud.product.get_multi(db=db)
    if not results:
        return {"results": []}
    
    return {"results": list(results)}

#Caso de uso: Crear un producto nuevo en la base de datos
@router.post("/", status_code=201, response_model=Product, response_description="Product created")
def create_product(
    *,
    product: ProductCreate =  Body(
        ...,
        example={
        "id": 123,
        "name": "Clamato",
        "quantity": 15,
        "description": "Jugo de tomate preparado con almejas y especias.",
        "price": 32.5,
        }
    ),
    
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
        
) -> Product:
    """
    Create a product. Only vendedor can create products
    """
    logger.debug(current_user.privilege)
    if current_user.privilege != 2 and current_user.privilege != 1:
        raise authorization_exception
    
    return crud.product.create(db=db, obj_in=product)



#Caso de uso: Eliminar un producto de la base de datos
@router.delete("/{product_id}", status_code=200)
def delete_product(
    *,
    product_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Delete a product. Only vendedor can delete products
    """
    if current_user.privilege != 2 and current_user.privilege != 1:
        raise authorization_exception
    
    crud.product.remove(db=db, id=product_id)

    return {"message": "Product deleted"}
    
#Caso de uso: Actualizar un producto de la base de datos
@router.put("/{product_id}", status_code=200, response_model=Product)
def update_product(
    *,
    product_id: int,
    product_in: ProductUpdate = Body(
        ...,
        example={
        "id": 123,
        "name": "Clamato",
        "quantity": 15,
        "description": "Jugo de tomate preparado con almejas y especias.",
        "price": 32.5,
        }
    ),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Product:
    """
    Update a product. Only client cannot update products
    """
    if current_user.privilege != 2 and current_user.privilege != 1:
        raise authorization_exception
    
    product = crud.product.get(db=db, id=product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )
    
    product = crud.product.update(db=db, db_obj=product, obj_in=product_in)
    return product
    