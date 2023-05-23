from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.schemas.report import (
    ReportSearchResults,
    Report,
    ReportCreate,
    ReportUpdate
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


@router.get("/all_report", status_code=200, response_model=ReportSearchResults)
def get_all_report(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """
    Show all sales reports to the admin, returns error if the user isn't admin
    """
    if current_user.privilege != 1:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to perform this action",
        )
    results = crud.report.get_multi(db=db)
    if not results:
        return {"results": list()}
    logger.debug(results[0].owner_id)
    return {"results": list(results)}

"""
@router.get("/get_report", status_code=201, response_model=ReportSearchResults)
def get_own_reports(
    *,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    reports = current_user.reports
    print(reports)
    if not reports:
        return {"results": list()}

    return {"results": list(reports)}
"""


@router.post("/make_report", status_code=201, response_model=Report)
def create_own_report(
    *,
    report_in: ReportCreate = Body(
        ...,
        example={
            "notas": "Cobro pal SAT",
            "total": 1000,
            "owner_id":3,
            "rfc": "ALALLALALALA",
        }
    ),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Report:
    """
    Create a new report in the database. Used by vendedor
    """
    
    if report_in.owner_id != current_user.id:
        raise HTTPException(
            status_code=401,
            detail="You can only create sale reports for yourself",
        )
    
    report = crud.report.create(db=db, obj_in=report_in)

    return report


"""
@router.put("/{report_id}", status_code=201, response_model=Report)
def update_client_report(
    *,
    report_id: int,
    report_in: ReportUpdate = Body(
        ...,
        example={
            "notas": "Pendiente a presentar declaracion en el SAT",
            "total": 1000,
            "rfc": "RFCRFCRFCRFCR",
        }
    ),

    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    #Update a report in the database. Only used by admin and vendedor
    
    if current_user.privilege != 1 and current_user.privilege != 2:
        raise HTTPException(
            status_code=401,
            detail="Not authorized to update report",
        )
    
    report = crud.report.get(db=db, id=report_id)

    if not report:
        raise HTTPException(
            status_code=404,
            detail="report not found",
        )

    report = crud.report.update(db=db, db_obj=report, obj_in=report_in)
    return report
"""

"""
@router.delete("/{report_id}", status_code=200, response_model=Report)
def delete_client_report(
    *,
    report_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:

    if current_user.privilege != 1 and current_user.privilege != 2:
        raise HTTPException(
            status_code=401,
            detail="Not authorized to delete a sale report",
        )

    report = crud.report.get(db=db, id=report_id)
    if not report:
        raise HTTPException(
            status_code=404,
            detail="sale report not found",
        )
    report = crud.report.remove(db=db, id=report_id)
    return report
"""