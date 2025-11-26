
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.due_diligence import DueDiligenceType, DueDiligenceFile

router=APIRouter(prefix="/due-diligence",tags=["due diligence"])

@router.post("/admin/add-type")
def add_type(project_id:int,title:str,db:Session=Depends(get_db)):
    t=DueDiligenceType(project_id=project_id,title=title)
    db.add(t); db.commit(); db.refresh(t)
    return {"id":t.id}

@router.delete("/admin/delete-type/{tid}")
def delete_type(tid:int,db:Session=Depends(get_db)):
    db.query(DueDiligenceType).filter_by(id=tid).delete()
    db.commit()
    return {"status":"deleted"}

@router.post("/upload")
def upload_dd(applicant_id:int,type_id:int,file:UploadFile=File(...),db:Session=Depends(get_db)):
    save_path=f"uploads/due_diligence/{applicant_id}_{file.filename}"
    with open(save_path,"wb") as f: f.write(file.file.read())
    d=DueDiligenceFile(applicant_id=applicant_id,type_id=type_id,file_path=save_path)
    db.add(d); db.commit(); db.refresh(d)
    return {"file_id":d.id}

@router.get("/view/{applicant_id}")
def view(applicant_id:int,db:Session=Depends(get_db)):
    files=db.query(DueDiligenceFile).filter_by(applicant_id=applicant_id).all()
    return files
