
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.project import Project
from datetime import date

router=APIRouter(prefix="/projects",tags=["projects"])

@router.post("/create")
def create_project(title:str, description:str="", financial_deadline:date=None,
                   narrative_deadline:date=None, inquiry_deadline:date=None,
                   reporting_months:int=6, db:Session=Depends(get_db)):
    p=Project(title=title,description=description,
              financial_deadline=financial_deadline,
              narrative_deadline=narrative_deadline,
              inquiry_deadline=inquiry_deadline,
              reporting_months=reporting_months)
    db.add(p); db.commit(); db.refresh(p)
    return {"project_id":p.id}

@router.post("/{pid}/edit")
def edit_project(pid:int,data:dict,db:Session=Depends(get_db)):
    p=db.query(Project).filter_by(id=pid).first()
    for k,v in data.items():
        setattr(p,k,v)
    db.commit()
    return {"status":"updated"}

@router.get("/list")
def list_projects(db:Session=Depends(get_db)):
    return db.query(Project).all()

@router.post("/{pid}/deactivate")
def deactivate(pid:int,db:Session=Depends(get_db)):
    p=db.query(Project).filter_by(id=pid).first()
    p.active=False; db.commit()
    return {"status":"inactive"}
