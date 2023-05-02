# WARNING: This is not authentication, 
# this is for admin functionalities like 
# searching users, creating vendors or displaying users in a table.

from fastapi import APIRouter

from app.schemas.user import (
    UserSearchResults,
)

router = APIRouter()


@router.get("/", status_code=200, response_model=UserSearchResults)
def get_vendedores( ) -> dict:
    """
    Get all vendedores
    """

    return {"results": []}



