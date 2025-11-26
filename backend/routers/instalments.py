
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import os
from datetime import date
from database import get_db
from models.request_instalment import RequestInstalment
from models.contract import Contract

router = APIRouter(prefix="/instalments", tags=["instalments"])

@router.post("/create")
def create_instalment(applicant_id:int,project_id:int,contract_id:int,
                      amount_number:int,amount_words:str,
                      account_name:str,account_number:str,iban:str,swift:str,bank_name:str,
                      db:Session=Depends(get_db)):

    previous=db.query(RequestInstalment).filter_by(applicant_id=applicant_id,project_id=project_id).count()
    instalment_number=previous+1
    request_number=f"REQ-{project_id}-{applicant_id}-{instalment_number}"

    r=RequestInstalment(
        applicant_id=applicant_id,project_id=project_id,contract_id=contract_id,
        instalment_number=instalment_number,
        request_number=request_number,
        amount_number=amount_number,
        amount_words=amount_words,
        account_name=account_name,
        account_number=account_number,
        iban=iban,
        swift=swift,
        bank_name=bank_name,
        date=date.today()
    )

    db.add(r); db.commit(); db.refresh(r)
    return {"instalment_id":r.id,"request_number":request_number}

@router.post("/upload-signed/{instalment_id}")
def upload_signed(instalment_id:int,file:UploadFile=File(...),db:Session=Depends(get_db)):
    path=f"uploads/instalments/signed/{instalment_id}_{file.filename}"
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,"wb") as f:f.write(file.file.read())
    r=db.query(RequestInstalment).filter_by(id=instalment_id).first()
    r.signed_doc_path=path
    db.commit()
    return {"status":"uploaded"}

@router.post("/submit/{instalment_id}")
def submit(instalment_id:int,db:Session=Depends(get_db)):
    r=db.query(RequestInstalment).filter_by(id=instalment_id).first()
    r.status="SUBMITTED"
    db.commit()
    return {"status":"submitted"}

@router.post("/admin/approve/{instalment_id}")
def approve(instalment_id:int,db:Session=Depends(get_db)):
    r=db.query(RequestInstalment).filter_by(id=instalment_id).first()
    r.status="APPROVED"
    db.commit()
    return {"status":"approved"}

@router.post("/admin/reject/{instalment_id}")
def reject(instalment_id:int,db:Session=Depends(get_db)):
    r=db.query(RequestInstalment).filter_by(id=instalment_id).first()
    r.status="REJECTED"
    db.commit()
    return {"status":"rejected"}

@router.get("/history/{applicant_id}/{project_id}")
def history(applicant_id:int,project_id:int,db:Session=Depends(get_db)):
    return db.query(RequestInstalment).filter_by(applicant_id=applicant_id,project_id=project_id).all()
