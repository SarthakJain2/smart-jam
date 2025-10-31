from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base
import enum
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .db import Base
from sqlalchemy.orm import relationship

class ApplicationStatus(str, enum.Enum):
    APPLIED = "Applied"
    OA = "OA"
    INTERVIEW = "Interview"
    OFFER = "Offer"
    REJECTED = "Rejected"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # reset
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)

    applications = relationship("Application", back_populates="user")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    company = Column(String(255), index=True, nullable=False)
    role = Column(String(255), index=True, nullable=False)
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.APPLIED, index=True)
    date_applied = Column(DateTime, default=datetime.utcnow)
    recruiter = Column(String(255))
    notes = Column(Text)
    deadline = Column(DateTime, nullable=True)
    resume_text = Column(Text, nullable=True)
    jd_text = Column(Text, nullable=True)

    # ✅ rename from `owner` to `user`
    user = relationship("User", back_populates="applications")

    matches = relationship("Match", back_populates="application", cascade="all, delete-orphan")

class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), index=True)
    score = Column(Float)
    skills_present = Column(Text) # comma-separated
    skills_missing = Column(Text) # comma-separated
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="matches")