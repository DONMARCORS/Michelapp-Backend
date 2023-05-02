from fastapi import APIRouter, HTTPException
from app.schemas.order import (
    OrderSearchResults,
)

router = APIRouter()

authorization_exception = HTTPException(
        status_code=403,
        detail="Not authorized to perform this action",
    )

@router.get("/", status_code=200, response_model=OrderSearchResults)
def create_sell_report(
) -> dict:
    """
    Create a sell report
    """

    return {"results": []}