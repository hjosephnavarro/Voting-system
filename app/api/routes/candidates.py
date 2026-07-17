from fastapi import APIRouter, HTTPException, status
from app.services.candidate_service import CandidateService
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse, CandidateListResponse
from app.exceptions.custom_exceptions import DuplicateEmailError, CandidateNotFoundError, DatabaseError

router = APIRouter(prefix="/candidates", tags=["Candidatos"])

# PRIMERO: Rutas específicas (sin parámetros)
@router.get("/", response_model=CandidateListResponse)
async def get_all_candidates():
    """Obtener todos los candidatos"""
    service = CandidateService()
    try:
        candidates = service.get_all_candidates()
        return CandidateListResponse(total=len(candidates), candidates=candidates)
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

@router.post("/", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(candidate_data: CandidateCreate):
    """Registrar un nuevo candidato"""
    service = CandidateService()
    try:
        result = service.create_candidate(candidate_data)
        return result
    except DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

# DESPUÉS: Rutas con parámetros
@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate_by_id(candidate_id: int):
    """Obtener un candidato por su ID"""
    service = CandidateService()
    try:
        candidate = service.get_candidate_by_id(candidate_id)
        return candidate
    except CandidateNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(candidate_id: int, candidate_data: CandidateUpdate):
    """Actualizar un candidato"""
    service = CandidateService()
    try:
        candidate = service.update_candidate(candidate_id, candidate_data)
        return candidate
    except CandidateNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DuplicateEmailError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()

@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(candidate_id: int):
    """Eliminar un candidato"""
    service = CandidateService()
    try:
        service.delete_candidate(candidate_id)
    except CandidateNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        service.close()