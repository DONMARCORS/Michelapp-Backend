# WARNING: This is not authentication, 
# this is for admin functionalities like 
# searching users, creating vendors or displaying users in a table.

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.user import (
    User,
    UserSearchResults,
)

router = APIRouter()

@router.get("/search/", status_code=200, response_model=UserSearchResults)
def search_users(
    *,
    keyword: str = Query(None, min_length=3, example="alex"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),

) -> dict:
    """
    Search for users based on first_name keyword
    """

    if current_user.privilege != 1:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to perform this action",
        )


    users = crud.user.get_multi(db=db, limit=max_results)
    results = filter(lambda user: keyword.lower() in user.first_name.lower(), users)

    return {"results": list(results)}

@router.get("/vendedores", status_code=200, response_model=UserSearchResults)
def get_vendedores(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    
) -> dict:
    """
    Get all vendedores
    """

    if current_user.privilege != 1:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to perform this action",
        )

    users = crud.user.get_multi(db=db)
    results = filter(lambda user: 2 == user.privilege, users)

    return {"results": list(results)}

@router.get("/clientes", status_code=200, response_model=UserSearchResults)
def get_clientes(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    
) -> dict:
    """
    get all users
    """

    if current_user.privilege != 1:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to perform this action",
        )

    users = crud.user.get_multi(db=db)
    results = filter(lambda user: 3 == user.privilege, users)

    return {"results": list(results)}
