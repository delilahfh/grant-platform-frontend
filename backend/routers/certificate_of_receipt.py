
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from datetime import date
import os

from database import get_db
from models.certificate_template import CertificateTemplate
from models.certificate_of_receipt import CertificateOfReceipt

router = APIRouter(prefix="/cor", tags=["certificate of receipt"])

# Admin: upload universal or per-project template
@router.post("/admin/upload-template")
def upload_template(title: str, file: UploadFile = File(...), project_id: int | None = None, db: Session = Depends(get_db)):
    path = f"uploads/cor/templates/{'global' if project_id is None else project_id}_{file.filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(file.file.read())
    t = CertificateTemplate(project_id=project_id, title=title, template_path=path)
    db.add(t)
    db.commit()
    db.refresh(t)
    return {"template_id": t.id}

# Applicant: create certificate draft
@router.post("/create")
def create_cor(applicant_id: int, project_id: int, procurement_id: int, items_text: str, cor_date: date | None = None, db: Session = Depends(get_db)):
    c = CertificateOfReceipt(
        applicant_id=applicant_id,
        project_id=project_id,
        procurement_id=procurement_id,
        date=cor_date or date.today(),
        items_text=items_text,
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"cor_id": c.id}

# System: generate docx placeholder (to later merge template + data)
@router.post("/generate/{cor_id}")
def generate_doc(cor_id: int, db: Session = Depends(get_db)):
    c = db.query(CertificateOfReceipt).filter_by(id=cor_id).first()
    if not c:
        return {"error": "not_found"}

    path = f"uploads/cor/generated/{cor_id}.docx"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # Placeholder empty file – real merge logic can be added later
    with open(path, "wb") as f:
        f.write(b"")
    c.generated_doc_path = path
    db.commit()
    return {"generated_path": path}

# Applicant: upload signed certificate
@router.post("/upload-signed/{cor_id}")
def upload_signed(cor_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    c = db.query(CertificateOfReceipt).filter_by(id=cor_id).first()
    if not c:
        return {"error": "not_found"}
    path = f"uploads/cor/signed/{cor_id}_{file.filename}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(file.file.read())
    c.signed_doc_path = path
    c.status = "SUBMITTED"
    db.commit()
    return {"status": "submitted"}

# Admin: approve / reject
@router.post("/admin/approve/{cor_id}")
def approve(cor_id: int, db: Session = Depends(get_db)):
    c = db.query(CertificateOfReceipt).filter_by(id=cor_id).first()
    if not c:
        return {"error": "not_found"}
    c.status = "APPROVED"
    db.commit()
    return {"status": "approved"}

@router.post("/admin/reject/{cor_id}")
def reject(cor_id: int, db: Session = Depends(get_db)):
    c = db.query(CertificateOfReceipt).filter_by(id=cor_id).first()
    if not c:
        return {"error": "not_found"}
    c.status = "REJECTED"
    db.commit()
    return {"status": "rejected"}

# History per applicant + project
@router.get("/history/{applicant_id}/{project_id}")
def history(applicant_id: int, project_id: int, db: Session = Depends(get_db)):
    lst = db.query(CertificateOfReceipt).filter_by(applicant_id=applicant_id, project_id=project_id).all()
    return lst
