
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.narrative_report import NarrativeReport, NarrativeReportSection

router=APIRouter(prefix="/narrative-reports",tags=["narrative reports"])

@router.post("/create")
def create_report(applicant_id:int,project_id:int,period_start:str,period_end:str,db:Session=Depends(get_db)):
    versions=db.query(NarrativeReport).filter_by(applicant_id=applicant_id,project_id=project_id).all()
    new_v=len(versions)+1
    r=NarrativeReport(applicant_id=applicant_id,project_id=project_id,version_number=new_v,
                      period_start=period_start,period_end=period_end)
    db.add(r); db.commit(); db.refresh(r)
    return {"report_id":r.id}

@router.post("/add-section")
def add_section(report_id:int,title:str,kpi:str,activity:str,status:str,
                date_of_completion:str,related_budget_line:str,description:str,db:Session=Depends(get_db)):
    s=NarrativeReportSection(report_id=report_id,title=title,kpi=kpi,activity=activity,
                             status=status,date_of_completion=date_of_completion,
                             related_budget_line=related_budget_line,description=description)
    db.add(s); db.commit(); db.refresh(s)
    return {"section_id":s.id}

@router.post("/submit/{report_id}")
def submit(report_id:int,db:Session=Depends(get_db)):
    r=db.query(NarrativeReport).filter_by(id=report_id).first()
    r.status="SUBMITTED"; db.commit()
    return {"status":"submitted"}

@router.post("/admin/{report_id}/accept")
def accept(report_id:int,db:Session=Depends(get_db)):
    r=db.query(NarrativeReport).filter_by(id=report_id).first()
    r.status="ACCEPTED"; db.commit()
    return {"status":"accepted"}

@router.post("/admin/{report_id}/reject")
def reject(report_id:int,db:Session=Depends(get_db)):
    r=db.query(NarrativeReport).filter_by(id=report_id).first()
    r.status="REJECTED"; db.commit()
    return {"status":"rejected"}

@router.get("/view/{report_id}")
def view(report_id:int,db:Session=Depends(get_db)):
    r=db.query(NarrativeReport).filter_by(id=report_id).first()
    sections=db.query(NarrativeReportSection).filter_by(report_id=report_id).all()
    return {"report":r,"sections":sections}
