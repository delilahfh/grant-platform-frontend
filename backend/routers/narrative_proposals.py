
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.narrative_proposal import NarrativeProposal, NarrativeProposalVersion, NarrativeSection, NarrativeEntry
from models.project import Project
from datetime import datetime

router=APIRouter(prefix="/narrative-proposals",tags=["narrative proposals"])

@router.post("/create")
def create_narrative(applicant_id:int, project_id:int, db:Session=Depends(get_db)):
    existing=db.query(NarrativeProposal).filter_by(applicant_id=applicant_id,project_id=project_id).first()
    if existing:
        return {"proposal_id":existing.id}
    p=NarrativeProposal(applicant_id=applicant_id,project_id=project_id)
    db.add(p); db.commit(); db.refresh(p)
    v=NarrativeProposalVersion(proposal_id=p.id,version_number=1)
    db.add(v); db.commit()
    return {"proposal_id":p.id,"version_id":v.id}

@router.post("/{proposal_id}/amend")
def amend(proposal_id:int, db:Session=Depends(get_db)):
    versions=db.query(NarrativeProposalVersion).filter_by(proposal_id=proposal_id).all()
    orig=versions[-1]
    new_v=NarrativeProposalVersion(proposal_id=proposal_id,version_number=len(versions)+1)
    db.add(new_v); db.commit(); db.refresh(new_v)
    entries=db.query(NarrativeEntry).filter_by(version_id=orig.id).all()
    for e in entries:
        db.add(NarrativeEntry(version_id=new_v.id,section_id=e.section_id,content=e.content))
    db.commit()
    return {"version_id":new_v.id}

@router.post("/version/{version_id}/submit")
def submit(version_id:int,db:Session=Depends(get_db)):
    v=db.query(NarrativeProposalVersion).filter_by(id=version_id).first()
    p=db.query(NarrativeProposal).filter_by(id=v.proposal_id).first()
    proj=db.query(Project).filter_by(id=p.project_id).first()
    v.status="SUBMITTED"
    if proj.narrative_deadline and datetime.utcnow().date()>proj.narrative_deadline:
        v.deadline_locked=True
    db.commit()
    return {"status":"submitted"}

@router.post("/admin/sections/add")
def add_section(project_id:int,title:str,order:int,db:Session=Depends(get_db)):
    s=NarrativeSection(project_id=project_id,title=title,order=order)
    db.add(s); db.commit(); db.refresh(s)
    return {"id":s.id}

@router.post("/version/{version_id}/section/{section_id}/edit")
def edit_entry(version_id:int,section_id:int,content:str,db:Session=Depends(get_db)):
    e=db.query(NarrativeEntry).filter_by(version_id=version_id,section_id=section_id).first()
    if not e:
        e=NarrativeEntry(version_id=version_id,section_id=section_id,content=content)
        db.add(e)
    else:
        e.content=content
    db.commit()
    return {"status":"updated"}

@router.get("/version/{version_id}")
def view(version_id:int,db:Session=Depends(get_db)):
    sections=db.query(NarrativeSection).order_by(NarrativeSection.order).all()
    out=[]
    for s in sections:
        e=db.query(NarrativeEntry).filter_by(version_id=version_id,section_id=s.id).first()
        out.append({"section":s.title,"content":e.content if e else "EMPTY"})
    return out
