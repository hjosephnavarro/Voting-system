from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class VoterBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr

class VoterCreate(VoterBase):
    pass

class VoterUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None

class VoterResponse(VoterBase):
    id: int
    has_voted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class VoterListResponse(BaseModel):
    total: int
    voters: list[VoterResponse]