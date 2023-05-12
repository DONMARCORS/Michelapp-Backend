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



