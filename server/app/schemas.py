from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List, Literal

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class ApplicationBase(BaseModel):
    company: str
    role: str
    status: Literal["Applied","OA","Interview","Offer","Rejected"] = "Applied"
    recruiter: Optional[str] = None
    notes: Optional[str] = None
    deadline: Optional[datetime] = None

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationOut(ApplicationBase):
    id: int
    date_applied: datetime
    class Config:
        from_attributes = True

class MatchRequest(BaseModel):
    resume_text: str = Field(min_length=20)
    jd_text: str = Field(min_length=20)

class MatchOut(BaseModel):
    id: int
    score: float
    skills_present: List[str]
    skills_missing: List[str]
    created_at: datetime
    class Config:
        from_attributes = True