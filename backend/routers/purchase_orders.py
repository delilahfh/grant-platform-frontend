
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.purchase_order import PurchaseOrder
import os

router=APIRouter(prefix="/purchase-orders",tags=["purchase orders"])

@router.post("/create")
def create_po(procurement_id:int,total_price:int,delivery_time:str,delivery_conditions:str,
              warranty:str,place_of_delivery:str,payment_schedule:str,db:Session=Depends(get_db)):
    po=PurchaseOrder(procurement_id=procurement_id,total_price=total_price,
                     delivery_time=delivery_time,delivery_conditions=delivery_conditions,
                     warranty=warranty,place_of_delivery=place_of_delivery,
                     payment_schedule=payment_schedule)
    db.add(po); db.commit(); db.refresh(po)
    return {"purchase_order_id":po.id}

@router.post("/upload/{po_id}")
def upload_po(po_id:int,file:UploadFile=File(...),db:Session=Depends(get_db)):
    path=f"uploads/purchase_orders/{po_id}_{file.filename}"
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,"wb") as f:f.write(file.file.read())
    po=db.query(PurchaseOrder).filter_by(id=po_id).first()
    po.file_path=path
    db.commit()
    return {"status":"uploaded"}

@router.get("/view/{po_id}")
def view(po_id:int,db:Session=Depends(get_db)):
    return db.query(PurchaseOrder).filter_by(id=po_id).first()
