# WARNING: This is not authentication, 
# this is for admin functionalities like 
# searching users, creating vendors or displaying users in a table.
import logging

from fastapi import APIRouter, Depends, HTTPException, Body

from sqlalchemy.orm import Session
from app import crud
from app.api import deps

from app.schemas.user import (
    User,
    UserSearchResults,
    UserUpdate,
    UserCreate
)

logger = logging.getLogger(__name__)
router = APIRouter()

authorization_exception = HTTPException(
        status_code=403,
        detail="Not authorized to perform this action",
    )

# Caso de uso ver vendedores (administrador) (Isaías Castrejón)
@router.get("/", status_code=200, response_model=UserSearchResults)
def get_vendedores(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    
 ) -> dict:
    """
    Get all vendedores
    """

    if current_user.privilege != 1:
        raise authorization_exception

    users = crud.user.get_multi(db)

    #filter to only users priviledge 2
    vendors = []
    for user in users:
        if user.privilege == 2:
            vendors.append(user)
    
    return {"results": vendors}

# Caso de uso actualizar vendedor (administrador) (Isaías Castrejón)
@router.put("/{vendor_id}", status_code=200, response_model=User)
def update_vendedor(
    *,
    vendor_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    user_in: UserUpdate,
    
 ) -> dict:
    """
    Update vendedor
    """

    if current_user.privilege != 1:
        raise authorization_exception

    user = crud.user.get(db, id=vendor_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = crud.user.update(db, db_obj=user, obj_in=user_in)

    return user

# Caso de uso: agregar vendedor (administrador) (Isaías Castrejón)
@router.post("/", status_code=201, response_model=User, response_description="Vendor created")
def create_vendedor(
    *,
    user_in: UserCreate = Body(
        ...,
        example={
            "first_name": "Bob",
            "last_name": "Peters",
            "email": "bobp@mail.com",
            "birthday": "2023-05-20",
            "address": "CDMX",
            "privilege": 2,
            "password": "password"
        }
    ),
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
) -> User:
    """
    Create a vendor
    """

    # Checamos si el usuario actual es administrador.
    if current_user.privilege != 1:
        raise authorization_exception
    logger.info("Creating vendor")
    # Checamos que el privilegio de el usuario por crear sea 2 (vendedor)
    if user_in.privilege != 2:
        raise HTTPException(status_code=400, detail="Cannot create vendor with privilege other than 2.")
    # Checamos que el correo no esté en uso
    email = crud.user.get_by_email(db, email=user_in.email)
    if email:
        raise HTTPException(status_code=400, detail="Email already in use.")
    # Creamos al vendedor
    vendor = crud.user.create(db, obj_in=user_in)
    return vendor

#Caso de uso: eliminar vendedor (administrador) (Isaías Castrejón)
@router.delete("/{vendor_id}", status_code=204, response_description="Vendor deleted")
def delete_vendor(
    *,
    db: Session = Depends(deps.get_db),
    vendor_id = int,
    current_user: User = Depends(deps.get_current_user)
) -> None:
    """
    Delete a vendor
    """

    if current_user.privilege != 1:
        raise authorization_exception
    
    found = crud.user.get(db, id=vendor_id)

    if not found:
        raise HTTPException(status_code=404, detail="Vendor not found.")
    
    if found.privilege != 2:
        raise HTTPException(status_code=400, detail="User is not a vendor.")
    
    crud.user.remove(db, id=vendor_id)