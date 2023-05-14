# WARNING: This is not authentication, 
# this is for admin/vendor functionalities like 
# searching clients, or displaying clients in a table.


from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from app import crud
from app.api import deps
from app.schemas.user import (
    User,
    UserSearchResults,
    UserCreate
)

from sqlalchemy.orm import Session

router = APIRouter()

authorization_exception = HTTPException(
        status_code=403,
        detail="Not authorized to perform this action",
    )


@router.get("/", status_code=200, response_model=UserSearchResults)
def get_clientes() -> dict:
    """
    Get all clients
    """

    return {"results": []}


# Caso de uso: Crear una cuenta del cliente
@router.post("/", status_code=200, response_model=User)
def create_cliente(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    user_in: UserCreate,

) -> dict:
    """
    Create a client
    """

    if current_user.privilege != 3:
        raise authorization_exception






