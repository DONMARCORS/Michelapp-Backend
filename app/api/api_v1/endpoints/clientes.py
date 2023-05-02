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
)

from sqlalchemy.orm import Session

router = APIRouter()

authorization_exception = HTTPException(
        status_code=403,
        detail="Not authorized to perform this action",
    )

@router.get("/search/", status_code=200, response_model=UserSearchResults)
def search_clients(
    *,
    first_name: Optional[str] = Query(None, min_length=3, example="joe"),
    last_name: Optional[str] = Query(None, min_length=3, example="smith"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),

) -> dict:
    """
    Search for clients based on first_name and last_name

    """

    if current_user.privilege != 1:
        raise authorization_exception

    users = crud.user.get_multi(db=db, limit=max_results)
    results = []
    for user in users:
        if user.privilege != 3:
            continue
        if first_name is not None and first_name.lower() not in user.first_name.lower():
            continue
        if last_name is not None and last_name.lower() not in user.last_name.lower():
            continue
        results.append(user)
    return {"results": list(results)}


@router.get("/", status_code=200, response_model=UserSearchResults)
def get_clientes() -> dict:
    """
    Get all clients
    """

    return {"results": []}



