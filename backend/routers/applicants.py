
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.applicant_profile import ApplicantProfile
from utils.notifications import send_notification
from utils.email_sender import send_email
import jwt

SECRET="SECRET_KEY"

router=APIRouter(prefix="/applicants",tags=["applicants"])

def auth(token:str):
    try:
        return jwt.decode(token,SECRET,algorithms=["HS256"])
    except:
        raise HTTPException(401,"Invalid token")

@router.get("/me")
def get_my_profile(token:str,db:Session=Depends(get_db)):
    u=auth(token)
    p=db.query(ApplicantProfile).filter_by(user_id=u["id"]).first()
    return p

@router.post("/update")
def update_profile(token:str, data:dict, db:Session=Depends(get_db)):
    u=auth(token)
    p=db.query(ApplicantProfile).filter_by(user_id=u["id"]).first()
    for k,v in data.items():
        setattr(p,k,v)
    db.commit()
    return {"status":"updated"}

@router.post("/admin/ban")
def ban_user(user_id:int, db:Session=Depends(get_db)):
    u=db.query(User).filter_by(id=user_id).first()
    u.banned=True; db.commit()
    return {"status":"banned"}

@router.post("/admin/request-update")
def request_update(user_id:int, db:Session=Depends(get_db)):
    send_notification(user_id,"Please update your profile")
    return {"status":"requested"}

@router.get("/admin/export")
def export_users(db:Session=Depends(get_db)):
    users=db.query(User).all()
    return {"count":len(users)}
