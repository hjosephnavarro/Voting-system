from fastapi import APIRouter, HTTPException, status
from typing import List
from app.services.voter_service import VoterService
from app.schemas.voter import VoterCreate, VoterUpdate, VoterResponse, VoterListResponse
from app.exceptions.custom_exceptions import DuplicateEmailError, VoterNotFoundError, DatabaseError

router = APIRouter(prefix="/voters", tags=["Votantes"])

@router.post("/", response_model=VoterResponse, status_code=status.HTTP_201_CREATED)
async def create_voter(voter_data: VoterCreate):
    service = VoterService()
    try:
        result = service.create_voter(voter_data)
        return result
    except DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

@router.get("/", response_model=VoterListResponse)
async def get_all_voters():
    service = VoterService()
    try:
        voters = service.get_all_voters()
        return VoterListResponse(total=len(voters), voters=voters)
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

@router.get("/{voter_id}", response_model=VoterResponse)
async def get_voter_by_id(voter_id: int):
    service = VoterService()
    try:
        voter = service.get_voter_by_id(voter_id)
        return voter
    except VoterNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

@router.put("/{voter_id}", response_model=VoterResponse)
async def update_voter(voter_id: int, voter_data: VoterUpdate):
    service = VoterService()
    try:
        voter = service.update_voter(voter_id, voter_data)
        return voter
    except VoterNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

@router.delete("/{voter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_voter(voter_id: int):
    service = VoterService()
    try:
        service.delete_voter(voter_id)
    except VoterNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()