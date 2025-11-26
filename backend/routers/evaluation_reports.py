
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.evaluation_report import EvaluationReport, EvaluationScore

router=APIRouter(prefix="/evaluation",tags=["evaluation reports"])

@router.post("/create")
def create_report(procurement_id:int,eligibility:str,quality:str,preferential:str,risks:str,selected_supplier:str,db:Session=Depends(get_db)):
    r=EvaluationReport(procurement_id=procurement_id,eligibility=eligibility,quality=quality,preferential=preferential,risks=risks,selected_supplier=selected_supplier)
    db.add(r); db.commit(); db.refresh(r)
    return {"report_id":r.id}

@router.post("/add-score")
def add_score(report_id:int,supplier_name:str,score:int,db:Session=Depends(get_db)):
    s=EvaluationScore(report_id=report_id,supplier_name=supplier_name,score=score)
    db.add(s); db.commit(); db.refresh(s)
    return {"score_id":s.id}

@router.get("/view/{report_id}")
def view(report_id:int,db:Session=Depends(get_db)):
    r=db.query(EvaluationReport).filter_by(id=report_id).first()
    scores=db.query(EvaluationScore).filter_by(report_id=report_id).all()
    return {"report":r,"scores":scores}
