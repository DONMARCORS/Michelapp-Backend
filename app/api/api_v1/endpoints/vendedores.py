# WARNING: This is not authentication, 
# this is for admin functionalities like 
# searching users, creating vendors or displaying users in a table.

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app import crud
from app.api import deps

from app.schemas.user import (
    User,
    UserSearchResults,
    UserUpdate,
    UserCreate
)

router = APIRouter()

authorization_exception = HTTPException(
        status_code=403,
        detail="Not authorized to perform this action",
    )

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


@router.put("/{user_id}", status_code=200, response_model=User)
def update_vendedor(
    *,
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    user_in: UserUpdate,
    
 ) -> dict:
    """
    Update vendedor
    """

    if current_user.privilege != 1:
        raise authorization_exception

    user = crud.user.get(db, id=user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = crud.user.update(db, db_obj=user, obj_in=user_in)

    return user

# get, post , put , delete
@router.put("/", status_code=200, response_model=User)
def create_vendedor(
    *,
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)):

    if current_user.privilege != 1:
        raise authorization_exception
    user = crud.user.get(db=db, id= current_user.id)
    return user
