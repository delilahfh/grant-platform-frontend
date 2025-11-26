
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.payments import PaymentRecord
import os
from datetime import date

router=APIRouter(prefix="/payments",tags=["payments"])

@router.post("/add")
def add_payment(procurement_id:int,amount:int,currency:str,payment_date:date,
                invoice:UploadFile=None,receipt:UploadFile=None,verification:UploadFile=None,
                db:Session=Depends(get_db)):
    pr=PaymentRecord(procurement_id=procurement_id,amount=amount,currency=currency,date=payment_date)
    db.add(pr); db.commit(); db.refresh(pr)

    base=f"uploads/payments/{pr.id}"
    os.makedirs(base,exist_ok=True)

    if invoice:
        p=os.path.join(base,"invoice_"+invoice.filename)
        with open(p,"wb") as f:f.write(invoice.file.read())
        pr.invoice_path=p

    if receipt:
        p=os.path.join(base,"receipt_"+receipt.filename)
        with open(p,"wb") as f:f.write(receipt.file.read())
        pr.receipt_path=p

    if verification:
        p=os.path.join(base,"verification_"+verification.filename)
        with open(p,"wb") as f:f.write(verification.file.read())
        pr.verification_path=p

    db.commit()
    return {"payment_id":pr.id}

@router.get("/view/{procurement_id}")
def view(procurement_id:int,db:Session=Depends(get_db)):
    return db.query(PaymentRecord).filter_by(procurement_id=procurement_id).all()
