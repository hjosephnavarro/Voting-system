from fastapi import APIRouter, HTTPException, status
from app.services.vote_service import VoteService
from app.schemas.vote import VoteCreate, VoteResponse, VoteDetailResponse, VoteStatisticsResponse
from app.exceptions.custom_exceptions import (
    VoterNotFoundError, CandidateNotFoundError, 
    VoterAlreadyVotedError, DatabaseError
)

router = APIRouter(prefix="/votes", tags=["Votos"])

# PRIMERO: Rutas específicas (sin parámetros)
@router.get("/statistics", response_model=VoteStatisticsResponse)
async def get_vote_statistics():
    """Obtener estadísticas de votación"""
    service = VoteService()
    try:
        stats = service.get_statistics()
        return stats
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

@router.get("/", response_model=list[VoteDetailResponse])
async def get_all_votes():
    """Obtener todos los votos emitidos"""
    service = VoteService()
    try:
        votes = service.get_all_votes()
        return votes
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

# DESPUÉS: Rutas con parámetros
@router.post("/", response_model=VoteResponse, status_code=status.HTTP_201_CREATED)
async def create_vote(vote_data: VoteCreate):
    """Emitir un nuevo voto"""
    service = VoteService()
    try:
        result = service.create_vote(vote_data)
        return result
    except (VoterNotFoundError, CandidateNotFoundError) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except VoterAlreadyVotedError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

@router.get("/{vote_id}", response_model=VoteDetailResponse)
async def get_vote_by_id(vote_id: int):
    """Obtener un voto por su ID"""
    service = VoteService()
    try:
        vote = service.get_vote_by_id(vote_id)
        return vote
    except DatabaseError as e:
        if "no encontrado" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

@router.delete("/{vote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vote(vote_id: int):
    """Eliminar un voto"""
    service = VoteService()
    try:
        service.delete_vote(vote_id)
    except DatabaseError as e:
        if "no encontrado" in str(e):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()