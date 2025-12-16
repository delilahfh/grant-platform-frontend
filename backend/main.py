import os
from typing import List, Optional
from datetime import date, datetime

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, Date, ForeignKey, JSON, Text, DateTime, Float
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

from passlib.context import CryptContext

# -----------------------------------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")  # local dev fallback
FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGINS", "*").split(",")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -----------------------------------------------------------------------------
# DATABASE SETUP
# -----------------------------------------------------------------------------
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -----------------------------------------------------------------------------
# DATABASE MODELS
# -----------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

    role = Column(String, default="applicant", nullable=False)  # "applicant" or "admin"
    is_banned = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    profile = relationship(
        "ApplicantProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


class ApplicantProfile(Base):
    __tablename__ = "applicant_profiles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    entity_type = Column(String, nullable=False)
    entity_name = Column(String, nullable=False)
    operation_locations = Column(JSON, nullable=False)  # List[str]
    detailed_address = Column(Text, nullable=False)

    fp1_name = Column(String, nullable=False)
    fp1_email = Column(String, nullable=False)
    fp1_dob = Column(Date, nullable=False)
    fp1_gender = Column(String, nullable=False)

    user = relationship("User", back_populates="profile")


class BudgetHeading(Base):
    __tablename__ = "budget_headings"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)


class BudgetLine(Base):
    __tablename__ = "budget_lines"
    id = Column(Integer, primary_key=True)

    heading_id = Column(Integer, ForeignKey("budget_headings.id"), nullable=False)
    item_name = Column(String, nullable=False)

    unit_amount = Column(Float, nullable=False)
    price_per_unit = Column(Float, nullable=False)

    co_financing_percent = Column(Integer, default=0, nullable=False)
    total_cost = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class Contract(Base):
    __tablename__ = "contracts"
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    signatory_name = Column(String, nullable=False)
    passport_number = Column(String, nullable=False)

    is_signed = Column(Boolean, default=False)
    generated_content = Column(Text, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)


class Procurement(Base):
    __tablename__ = "procurements"
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    budget_line_id = Column(Integer, ForeignKey("budget_lines.id"), nullable=True)

    type = Column(String, nullable=False)    # Product / Service / Works
    method = Column(String, nullable=False)  # SQ / 3Q / OLT

    description = Column(String, nullable=False)
    code = Column(String, index=True, nullable=False)

    status = Column(String, default="Draft", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


def create_tables_and_seed():
    Base.metadata.create_all(bind=engine)

    defaults = ["Machineries", "Works", "Licenses", "Training", "Consultancies", "Salaries", "Running Costs"]
    db = SessionLocal()
    try:
        existing = db.query(BudgetHeading).count()
        if existing == 0:
            for i, name in enumerate(defaults, start=1):
                db.add(BudgetHeading(name=name, display_order=i))
            db.commit()
    finally:
        db.close()

# -----------------------------------------------------------------------------
# APP INITIALIZATION
# -----------------------------------------------------------------------------
app = FastAPI(title="Grant Management Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in FRONTEND_ORIGINS] if FRONTEND_ORIGINS != ["*"] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables_and_seed()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(pw: str) -> str:
    return pwd_context.hash(pw)

# -----------------------------------------------------------------------------
# API SCHEMAS
# -----------------------------------------------------------------------------
class UserSignUp(BaseModel):
    email: EmailStr
    password: str

    entity_type: str
    entity_name: str
    locations: List[str]
    address: str

    fp1_name: str
    fp1_email: EmailStr
    fp1_dob: date
    fp1_gender: str


class BudgetHeadingOut(BaseModel):
    id: int
    name: str
    display_order: int

    class Config:
        from_attributes = True


class BudgetLineSchema(BaseModel):
    heading_id: int
    item_name: str
    unit_amount: float
    price_per_unit: float
    co_financing_percent: int = 0


class ContractSchema(BaseModel):
    user_id: int
    signatory_name: str
    passport_number: str


class ProcurementSchema(BaseModel):
    user_id: int
    budget_line_id: Optional[int] = None
    type: str
    method: str
    description: str


class ProcurementOut(BaseModel):
    id: int
    user_id: int
    budget_line_id: Optional[int]
    type: str
    method: str
    description: str
    code: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# -----------------------------------------------------------------------------
# HEALTH
# -----------------------------------------------------------------------------
@app.get("/health")
def health():
    return {"ok": True, "ts": datetime.utcnow().isoformat()}

# -----------------------------------------------------------------------------
# 1) SIGN UP
# -----------------------------------------------------------------------------
@app.post("/signup")
def sign_up(user_data: UserSignUp, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email exists")

    new_user = User(
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        role="applicant",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_profile = ApplicantProfile(
        user_id=new_user.id,
        entity_type=user_data.entity_type,
        entity_name=user_data.entity_name,
        operation_locations=user_data.locations,
        detailed_address=user_data.address,
        fp1_name=user_data.fp1_name,
        fp1_email=str(user_data.fp1_email),
        fp1_dob=user_data.fp1_dob,
        fp1_gender=user_data.fp1_gender,
    )
    db.add(new_profile)
    db.commit()

    return {"message": "Success", "user_id": new_user.id}

# -----------------------------------------------------------------------------
# 2) BUDGET
# -----------------------------------------------------------------------------
@app.get("/budget-headings", response_model=List[BudgetHeadingOut])
def get_headings(db: Session = Depends(get_db)):
    return db.query(BudgetHeading).order_by(BudgetHeading.display_order.asc()).all()

@app.post("/save-budget-line")
def save_budget_line(line: BudgetLineSchema, db: Session = Depends(get_db)):
    if line.unit_amount < 0 or line.price_per_unit < 0:
        raise HTTPException(status_code=400, detail="unit_amount and price_per_unit must be >= 0")

    heading = db.query(BudgetHeading).filter(BudgetHeading.id == line.heading_id).first()
    if not heading:
        raise HTTPException(status_code=404, detail="Heading not found")

    total = float(line.unit_amount) * float(line.price_per_unit)
    new_line = BudgetLine(
        heading_id=line.heading_id,
        item_name=line.item_name.strip(),
        unit_amount=float(line.unit_amount),
        price_per_unit=float(line.price_per_unit),
        co_financing_percent=int(line.co_financing_percent),
        total_cost=total,
    )
    db.add(new_line)
    db.commit()
    db.refresh(new_line)

    return {"message": "Saved", "total": total, "id": new_line.id}

# -----------------------------------------------------------------------------
# 3) ADMIN
# -----------------------------------------------------------------------------
@app.get("/admin/applications")
def get_all_applications(db: Session = Depends(get_db)):
    results = db.query(User, ApplicantProfile).join(ApplicantProfile, User.id == ApplicantProfile.user_id).all()
    data = []
    for user, profile in results:
        data.append({
            "user_id": user.id,
            "entity_name": profile.entity_name,
            "entity_type": profile.entity_type,
            "email": user.email,
            "is_banned": user.is_banned,
            "status": "Submitted",
        })
    return data

@app.post("/admin/impersonate/{user_id}")
def impersonate_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"Impersonating {user.email}", "redirect_url": "/application"}

@app.post("/admin/ban/{user_id}")
def ban_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.is_banned = not user.is_banned
        db.commit()
        return {"new_status": user.is_banned}
    raise HTTPException(status_code=404, detail="User not found")

# -----------------------------------------------------------------------------
# 4) CONTRACTS & PROCUREMENT
# -----------------------------------------------------------------------------
@app.post("/contracts/generate")
def generate_contract(data: ContractSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    template = "<h1>CONTRACT</h1><p>Between Donor and {name} ({passport}). Date: {date}</p>"
    content = template.format(
        name=data.signatory_name,
        passport=data.passport_number,
        date=date.today().isoformat(),
    )

    new_contract = Contract(
        user_id=data.user_id,
        signatory_name=data.signatory_name,
        passport_number=data.passport_number,
        generated_content=content,
    )
    db.add(new_contract)
    db.commit()
    db.refresh(new_contract)

    return {"content": content, "contract_id": new_contract.id}

@app.post("/procurement/create")
def create_procurement(data: ProcurementSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    count = (
        db.query(Procurement)
        .filter(Procurement.method == data.method, Procurement.user_id == data.user_id)
        .count()
    )
    next_num = str(count + 1).zfill(2)
    code = f"{data.method}{next_num}-{data.type}"

    new_proc = Procurement(
        user_id=data.user_id,
        budget_line_id=data.budget_line_id,
        type=data.type,
        method=data.method,
        description=data.description,
        code=code,
    )
    db.add(new_proc)
    db.commit()
    db.refresh(new_proc)

    return {"code": code, "procurement_id": new_proc.id}

@app.get("/procurements/{user_id}", response_model=List[ProcurementOut])
def get_procurements(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Procurement)
        .filter(Procurement.user_id == user_id)
        .order_by(Procurement.created_at.desc())
        .all()
    )
