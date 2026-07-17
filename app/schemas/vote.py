from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class VoteCreate(BaseModel):
    voter_id: int = Field(..., gt=0)
    candidate_id: int = Field(..., gt=0)

class VoteResponse(BaseModel):
    id: int
    voter_id: int
    candidate_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class VoteDetailResponse(BaseModel):
    id: int
    voter_name: str
    voter_email: str
    candidate_name: str
    candidate_party: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class CandidateResult(BaseModel):
    candidate_id: int
    candidate_name: str
    party: Optional[str]
    votes: int
    percentage: float

class VoteStatisticsResponse(BaseModel):
    total_voters: int
    total_voted: int
    total_candidates: int
    total_votes: int
    results: list[CandidateResult]