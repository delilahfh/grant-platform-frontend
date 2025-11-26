
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Header
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict
from datetime import datetime
import uuid

app = FastAPI(title="Grant App Backend – Skeleton")

# ===== In-memory stores (for local testing only) =====

users: List[Dict] = [
    {"id": "admin-1", "email": "admin@example.com", "password": "admin", "role": "admin"},
]

tokens: Dict[str, Dict] = {}

applications: List[Dict] = []
deadlines: List[Dict] = []
inquiries: List[Dict] = []


# ===== Helpers =====

def get_current_user(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    user = tokens.get(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

def require_admin(user = Depends(get_current_user)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    return user


# ===== Auth =====

@app.post("/register")
async def register(email: str, password: str, role: str = "applicant"):
    if any(u["email"] == email for u in users):
        raise HTTPException(status_code=400, detail="Email already registered")
    uid = str(uuid.uuid4())
    user = {"id": uid, "email": email, "password": password, "role": role}
    users.append(user)
    return {"id": uid, "email": email, "role": role}

@app.post("/login")
async def login(email: str, password: str):
    user = next((u for u in users if u["email"] == email and u["password"] == password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = f"token-{uuid.uuid4()}"
    tokens[token] = user
    return {"access_token": token, "token_type": "bearer", "role": user["role"]}

@app.get("/me")
async def me(user = Depends(get_current_user)):
    return {"id": user["id"], "email": user["email"], "role": user["role"]}

@app.get("/admin/me")
async def admin_me(user = Depends(require_admin)):
    return {"id": user["id"], "email": user["email"], "role": user["role"], "is_admin": True}


# ===== Simple endpoints matching frontend expectations =====

@app.post("/narrative-proposal")
async def narrative_proposal(data: Dict, user = Depends(get_current_user)):
    applications.append({"id": str(uuid.uuid4()), "type": "narrative_proposal", "data": data, "user": user["email"]})
    return {"status": "ok"}

@app.post("/financial-proposal")
async def financial_proposal(data: Dict, user = Depends(get_current_user)):
    applications.append({"id": str(uuid.uuid4()), "type": "financial_proposal", "data": data, "user": user["email"]})
    return {"status": "ok"}

@app.post("/financial-amendment")
async def financial_amendment(data: Dict, user = Depends(get_current_user)):
    applications.append({"id": str(uuid.uuid4()), "type": "financial_amendment", "data": data, "user": user["email"]})
    return {"status": "ok"}

@app.post("/financial-report")
async def financial_report(data: Dict, user = Depends(get_current_user)):
    applications.append({"id": str(uuid.uuid4()), "type": "financial_report", "data": data, "user": user["email"]})
    return {"status": "ok"}

@app.post("/narrative-report")
async def narrative_report(data: Dict, user = Depends(get_current_user)):
    applications.append({"id": str(uuid.uuid4()), "type": "narrative_report", "data": data, "user": user["email"]})
    return {"status": "ok"}

@app.post("/supporting-documents")
async def supporting_documents(
    mof: Optional[List[UploadFile]] = File(default=None),
    chamber: Optional[List[UploadFile]] = File(default=None),
    finance: Optional[List[UploadFile]] = File(default=None),
    other: Optional[List[UploadFile]] = File(default=None),
    user = Depends(get_current_user)
):
    return {"status": "ok"}

@app.post("/request-for-quotation")
async def request_for_quotation(data: Dict, user = Depends(get_current_user)):
    return {"status": "ok"}

@app.post("/evaluation-report")
async def evaluation_report(data: Dict, user = Depends(get_current_user)):
    return {"status": "ok"}

@app.post("/evaluation-annex")
async def evaluation_annex(data: Dict, user = Depends(get_current_user)):
    return {"status": "ok"}

@app.post("/procurement-contract")
async def procurement_contract(data: Dict, user = Depends(get_current_user)):
    return {"status": "ok"}

@app.post("/delivery-certificate")
async def delivery_certificate(data: Dict, user = Depends(get_current_user)):
    return {"status": "ok"}

@app.post("/certificate-of-receipt")
async def certificate_of_receipt(data: Dict, user = Depends(get_current_user)):
    return {"status": "ok"}

@app.post("/fund-request")
async def fund_request(data: Dict, user = Depends(get_current_user)):
    return {"status": "ok"}

@app.post("/grant-contract")
async def grant_contract(data: Dict, user = Depends(get_current_user)):
    return {"status": "ok"}


# ===== Deadlines =====

@app.get("/deadlines")
async def get_deadlines(admin = Depends(require_admin)):
    return deadlines

@app.post("/deadlines")
async def create_deadline(payload: Dict, admin = Depends(require_admin)):
    d = {
        "id": str(uuid.uuid4()),
        "title": payload.get("title"),
        "type": payload.get("type"),
        "project": payload.get("project"),
        "due_at": payload.get("due_at"),
        "active": True,
    }
    deadlines.append(d)
    return d

@app.patch("/deadlines/{deadline_id}")
async def update_deadline(deadline_id: str, payload: Dict, admin = Depends(require_admin)):
    for d in deadlines:
        if d["id"] == deadline_id:
            d.update(payload)
            return d
    raise HTTPException(status_code=404, detail="Not found")

@app.get("/my-deadlines")
async def my_deadlines(user = Depends(get_current_user)):
    # simple: return all active deadlines
    return [d for d in deadlines if d.get("active")]


# ===== Inquiries =====

@app.post("/inquiries")
async def create_inquiry(payload: Dict, user = Depends(get_current_user)):
    item = {
        "id": str(uuid.uuid4()),
        "user_email": user["email"],
        "application_id": payload.get("application_id"),
        "message": payload.get("message"),
        "created_at": datetime.utcnow().isoformat()
    }
    inquiries.append(item)
    return item

@app.get("/inquiries")
async def my_inquiries(user = Depends(get_current_user)):
    return [i for i in inquiries if i["user_email"] == user["email"]]

@app.get("/admin/inquiries")
async def admin_inquiries(admin = Depends(require_admin)):
    return inquiries


# ===== Authorized files & projects (stubs) =====

@app.get("/authorized-files")
async def authorized_files(user = Depends(get_current_user)):
    return [
        {"name": "Authorized_Budget.docx", "url": "#"},
        {"name": "Project_Description.docx", "url": "#"},
    ]

@app.get("/projects")
async def list_projects(admin = Depends(require_admin)):
    return []

@app.post("/projects")
async def create_project(admin = Depends(require_admin)):
    return {"status": "ok"}


# ===== Guidelines / Notifications stubs =====

@app.get("/guidelines")
async def guidelines(user = Depends(get_current_user)):
    return {"text": "Proposal development guidelines go here."}

@app.get("/notifications")
async def notifications(user = Depends(get_current_user)):
    return []

