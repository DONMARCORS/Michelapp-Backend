# WARNING: This is not authentications, 
# this is for admin functionalities like 
# searching users, or displaying users in a table.

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.schemas.user import (
    UserSearchResults,
)

router = APIRouter()
RECIPE_SUBREDDITS = ["recipes", "easyrecipes", "TopSecretRecipes"]

@router.get("/search/", status_code=200, response_model=UserSearchResults)
def search_recipes(
    *,
    keyword: str = Query(None, min_length=3, example="alex"),
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
) -> dict:
    """
    Search for users based on first_name keyword
    """
    users = crud.user.get_multi(db=db, limit=max_results)
    results = filter(lambda user: keyword.lower() in user.first_name.lower(), users)

    return {"results": list(results)}

@router.get("/vendedores", status_code=200, response_model=UserSearchResults)
def search_recipes(
    *,
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
    
) -> dict:
    """
    Search for users based on label keyword
    """
    users = crud.recipe.get_multi(db=db, limit=max_results)
    results = filter(lambda user: 2 == user.privilege, users)

    return {"results": list(results)}

@router.get("/usuarios", status_code=200, response_model=UserSearchResults)
def search_recipes(
    *,
    max_results: Optional[int] = 10,
    db: Session = Depends(deps.get_db),
    
) -> dict:
    """
    Search for users based on label keyword
    """
    users = crud.recipe.get_multi(db=db, limit=max_results)
    results = filter(lambda user: 3 == user.privilege, users)

    return {"results": list(results)}
