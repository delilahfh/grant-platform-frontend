
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
import json, os
from database import get_db
from models.contract_type import ContractType
from models.contract_field import ContractField
from models.contract import Contract

router = APIRouter(prefix="/contracts", tags=["contracts"])

# Admin uploads contract template
@router.post("/admin/upload-template")
def upload_template(project_id:int,title:str,file:UploadFile=File(...),db:Session=Depends(get_db)):
    path=f"uploads/contracts/templates/{project_id}_{file.filename}"
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,"wb") as f:f.write(file.file.read())
    ct=ContractType(project_id=project_id,title=title,template_path=path)
    db.add(ct); db.commit(); db.refresh(ct)
    return {"contract_type_id":ct.id}

# Admin sets rules
@router.post("/admin/set-rules")
def set_rules(contract_type_id:int, rules:dict, db:Session=Depends(get_db)):
    ct=db.query(ContractType).filter_by(id=contract_type_id).first()
    ct.rules_json=json.dumps(rules)
    db.commit()
    return {"status":"rules_saved"}

# Admin adds fields
@router.post("/admin/add-field")
def add_field(field_name:str,label:str,required:str,visible_for:str,db:Session=Depends(get_db)):
    f=ContractField(field_name=field_name,label=label,required=required,visible_for=visible_for)
    db.add(f); db.commit(); db.refresh(f)
    return {"field_id":f.id}

# Create contract for applicant
@router.post("/create")
def create_contract(applicant_id:int,project_id:int,db:Session=Depends(get_db)):
    c=Contract(applicant_id=applicant_id,project_id=project_id)
    db.add(c); db.commit(); db.refresh(c)
    return {"contract_id":c.id}
