from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.schemas.report import (
    ReportSearchResults,
)
from app.models.user import User
from app.api import deps
router = APIRouter()
import logging
logger = logging.getLogger(__name__)

authorization_exception = HTTPException(
        status_code=403,
        detail="Not authorized to perform this action",
    )


@router.get("/sale_report", status_code=200, response_model=ReportSearchResults)
def create_sale_report(
) -> dict:
    """
    Create a sale report
    """

    return {"results": []}

@router.get("/all_report", status_code=200, response_model=ReportSearchResults)
def get_all_report(
    *,
    db: Session = Depends(deps.get_db),
    #current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Show all sales reports to the admin, returns error if the user isn't admin
    """
    """
    if current_user.privilege != 1:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to perform this action",
        )
    """
    results = crud.report.get_multi(db=db)
    if not results:
        return {"results": list()}
    logger.debug(results[0].owner_id)
    return {"results": list(results)}


