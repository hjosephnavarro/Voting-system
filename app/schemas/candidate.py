from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class CandidateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    party: Optional[str] = Field(None, max_length=255)

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    party: Optional[str] = Field(None, max_length=255)

class CandidateResponse(CandidateBase):
    id: int
    votes: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class CandidateListResponse(BaseModel):
    total: int
    candidates: list[CandidateResponse]