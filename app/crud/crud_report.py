from app.crud.base import CRUDBase
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate

class CRUDReport(CRUDBase[Report, ReportCreate, ReportUpdate]):
    ...


report = CRUDReport(Report)