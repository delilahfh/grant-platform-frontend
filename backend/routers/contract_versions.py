
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import os
from database import get_db
from models.contract import Contract
from models.contract_version import ContractVersion

router = APIRouter(prefix="/contract-versions", tags=["contract versions"])

@router.post("/generate")
def generate_version(contract_id:int,version_number:int,db:Session=Depends(get_db)):
    path=f"uploads/contracts/generated/{contract_id}_v{version_number}.docx"
    os.makedirs(os.path.dirname(path),exist_ok=True)
    # placeholder file
    with open(path,"wb") as f:f.write(b"")
    v=ContractVersion(contract_id=contract_id,version_number=version_number,generated_doc_path=path)
    db.add(v); db.commit(); db.refresh(v)
    return {"version_id":v.id}

@router.post("/upload-signed/{version_id}")
def upload_signed(version_id:int,file:UploadFile=File(...),db:Session=Depends(get_db)):
    path=f"uploads/contracts/signed/{version_id}_{file.filename}"
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,"wb") as f:f.write(file.file.read())
    v=db.query(ContractVersion).filter_by(id=version_id).first()
    v.signed_doc_path=path
    db.commit()
    return {"status":"uploaded"}
