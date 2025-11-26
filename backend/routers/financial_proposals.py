
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.financial_proposal import FinancialProposal, FinancialProposalVersion, BudgetHeading, BudgetLine
from models.project import Project

router = APIRouter(prefix="/financial-proposals", tags=["financial proposals"])

# --- Create initial proposal ---
@router.post("/create")
def create_proposal(applicant_id: int, project_id: int, db: Session = Depends(get_db)):
    existing = db.query(FinancialProposal).filter_by(applicant_id=applicant_id, project_id=project_id).first()
    if existing:
        return {"proposal_id": existing.id}

    p = FinancialProposal(applicant_id=applicant_id, project_id=project_id)
    db.add(p); db.commit(); db.refresh(p)

    v = FinancialProposalVersion(proposal_id=p.id, version_number=1, is_original=True)
    db.add(v); db.commit()
    return {"proposal_id": p.id, "version_id": v.id}

# --- Amendment clone ---
@router.post("/{proposal_id}/amend")
def create_amendment(proposal_id: int, db: Session = Depends(get_db)):
    versions = db.query(FinancialProposalVersion).filter_by(proposal_id=proposal_id).all()
    original = versions[-1]
    new_vn = len(versions)+1

    new_v = FinancialProposalVersion(proposal_id=proposal_id, version_number=new_vn)
    db.add(new_v); db.commit(); db.refresh(new_v)

    # clone lines
    for line in db.query(BudgetLine).filter_by(version_id=original.id).all():
        db.add(BudgetLine(
            version_id=new_v.id,
            heading_id=line.heading_id,
            line_number=line.line_number,
            name=line.name,
            unit=line.unit,
            unit_cost=line.unit_cost,
            cofinancing=line.cofinancing
        ))
    db.commit()
    return {"version_id": new_v.id}

# --- Submit version ---
@router.post("/version/{version_id}/submit")
def submit_version(version_id:int, db:Session=Depends(get_db)):
    v=db.query(FinancialProposalVersion).filter_by(id=version_id).first()
    p=db.query(FinancialProposal).filter_by(id=v.proposal_id).first()
    proj=db.query(Project).filter_by(id=p.project_id).first()
    v.status="SUBMITTED"
    if proj.financial_deadline and datetime.utcnow().date()>proj.financial_deadline:
        v.deadline_locked=True
    db.commit()
    return {"status":"submitted"}

# --- Admin accept/reject ---
@router.post("/admin/{version_id}/accept")
def admin_accept(version_id:int, db:Session=Depends(get_db)):
    v=db.query(FinancialProposalVersion).filter_by(id=version_id).first()
    v.status="ACCEPTED"; db.commit()
    return {"status":"accepted"}

@router.post("/admin/{version_id}/reject")
def admin_reject(version_id:int, db:Session=Depends(get_db)):
    v=db.query(FinancialProposalVersion).filter_by(id=version_id).first()
    v.status="REJECTED"; db.commit()
    return {"status":"rejected"}

# --- Headings admin ---
@router.post("/admin/{project_id}/headings/add")
def add_heading(project_id:int,title:str,order:int,db:Session=Depends(get_db)):
    h=BudgetHeading(project_id=project_id,title=title,order=order)
    db.add(h); db.commit(); db.refresh(h)
    return {"id":h.id}

@router.post("/admin/headings/{hid}/edit")
def edit_heading(hid:int,title:str,order:int,db:Session=Depends(get_db)):
    h=db.query(BudgetHeading).filter_by(id=hid).first()
    h.title=title; h.order=order; db.commit()
    return {"status":"updated"}

@router.delete("/admin/headings/{hid}")
def delete_heading(hid:int,db:Session=Depends(get_db)):
    db.query(BudgetHeading).filter_by(id=hid).delete()
    db.commit(); return {"status":"deleted"}

# --- Budget lines ---
def gen_line_no(db, heading_id, version_id):
    h=db.query(BudgetHeading).filter_by(id=heading_id).first()
    c=db.query(BudgetLine).filter_by(heading_id=heading_id,version_id=version_id).count()
    return f"{h.order}.{c+1}"

@router.post("/version/{version_id}/lines/add")
def add_line(version_id:int, heading_id:int, name:str, unit:int, unit_cost:int, cofinancing:int, db:Session=Depends(get_db)):
    ln=gen_line_no(db,heading_id,version_id)
    l=BudgetLine(version_id=version_id,heading_id=heading_id,line_number=ln,name=name,unit=unit,unit_cost=unit_cost,cofinancing=cofinancing)
    db.add(l); db.commit(); db.refresh(l)
    return {"id":l.id,"line_number":ln}

@router.post("/lines/{lid}/edit")
def edit_line(lid:int,name:str,unit:int,unit_cost:int,cofinancing:int,db:Session=Depends(get_db)):
    l=db.query(BudgetLine).filter_by(id=lid).first()
    l.name=name; l.unit=unit; l.unit_cost=unit_cost; l.cofinancing=cofinancing
    db.commit(); return {"status":"updated"}

@router.delete("/lines/{lid}")
def delete_line(lid:int,db:Session=Depends(get_db)):
    db.query(BudgetLine).filter_by(id=lid).delete()
    db.commit(); return {"status":"deleted"}

# --- Get full version ---
@router.get("/version/{version_id}")
def get_version(version_id:int, db:Session=Depends(get_db)):
    v=db.query(FinancialProposalVersion).filter_by(id=version_id).first()
    headings=db.query(BudgetHeading).filter_by(project_id=v.proposal.project_id).order_by(BudgetHeading.order).all()
    out=[]
    for h in headings:
        lines=db.query(BudgetLine).filter_by(version_id=version_id,heading_id=h.id).all()
        out.append({
            "heading_id":h.id,
            "title":h.title,
            "lines":[{
                "line_id":l.id,
                "line_number":l.line_number,
                "name":l.name,
                "unit":l.unit,
                "unit_cost":l.unit_cost,
                "cofinancing":l.cofinancing
            } for l in lines]
        })
    return out
