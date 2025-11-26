
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.financial_report import FinancialReport, FinancialReportExpenditure
from models.project import Project

router=APIRouter(prefix="/financial-reports",tags=["financial reports"])

@router.post("/create")
def create_report(applicant_id:int,project_id:int,db:Session=Depends(get_db)):
    versions=db.query(FinancialReport).filter_by(applicant_id=applicant_id,project_id=project_id).all()
    new_v=len(versions)+1
    r=FinancialReport(applicant_id=applicant_id,project_id=project_id,version_number=new_v)
    db.add(r); db.commit(); db.refresh(r)
    return {"report_id":r.id}

@router.post("/add-expenditure")
def add_expenditure(report_id:int,procurement_code:str,date:str,budget_line:str,cost:int,currency:str,notes:str="",db:Session=Depends(get_db)):
    e=FinancialReportExpenditure(report_id=report_id,procurement_code=procurement_code,date=date,budget_line=budget_line,cost=cost,currency=currency,notes=notes)
    db.add(e); db.commit(); db.refresh(e)
    return {"entry_id":e.id}

@router.post("/submit/{report_id}")
def submit(report_id:int,db:Session=Depends(get_db)):
    r=db.query(FinancialReport).filter_by(id=report_id).first()
    r.status="SUBMITTED"; db.commit()
    return {"status":"submitted"}

@router.post("/admin/{report_id}/accept")
def accept(report_id:int,db:Session=Depends(get_db)):
    r=db.query(FinancialReport).filter_by(id=report_id).first()
    r.status="ACCEPTED"; db.commit()
    return {"status":"accepted"}

@router.post("/admin/{report_id}/reject")
def reject(report_id:int,db:Session=Depends(get_db)):
    r=db.query(FinancialReport).filter_by(id=report_id).first()
    r.status="REJECTED"; db.commit()
    return {"status":"rejected"}

@router.get("/view/{report_id}")
def view(report_id:int,db:Session=Depends(get_db)):
    r=db.query(FinancialReport).filter_by(id=report_id).first()
    exps=db.query(FinancialReportExpenditure).filter_by(report_id=report_id).all()
    return {"report":r,"expenditures":exps}
