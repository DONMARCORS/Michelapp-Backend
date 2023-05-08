# WARNING: This is not authentication, 
# this is for admin functionalities like 
# searching users, creating vendors or displaying users in a table.

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.user import (
    User,
    UserSearchResults,
)
from app.api import deps

router = APIRouter()

authorization_exception = HTTPException(
        status_code=403,
        detail="Not authorized to perform this action",
    )

@router.get("/", status_code=200, response_model=UserSearchResults)
def get_vendedores(

    current_user: User = Depends(deps.get_current_user),
 ) -> dict:
    """
    Get all vendedores
    """

    if current_user.privilege != 1:
        raise authorization_exception

    return {"results": []}



