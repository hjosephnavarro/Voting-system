from app.repositories.candidate_repository import CandidateRepository
from app.schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse
from app.exceptions.custom_exceptions import DuplicateEmailError, CandidateNotFoundError, DatabaseError

class CandidateService:
    def __init__(self):
        self.repository = CandidateRepository()
    
    def create_candidate(self, create_dto: CandidateCreate) -> CandidateResponse:
        try:
            if self.repository.exists_by_email(create_dto.email):
                raise DuplicateEmailError(f"El email {create_dto.email} ya está registrado")
            
            candidate_id = self.repository.create(
                create_dto.name, 
                create_dto.email, 
                create_dto.party
            )
            if not candidate_id:
                raise DatabaseError("Error al crear el candidato")
            
            candidate_data = self.repository.get_by_id(candidate_id)
            return self._to_response(candidate_data)
        except Exception as e:
            raise DatabaseError(f"Error al crear candidato: {str(e)}")
    
    def get_all_candidates(self) -> list[CandidateResponse]:
        try:
            candidates_data = self.repository.get_all()
            return [self._to_response(data) for data in candidates_data]
        except Exception as e:
            raise DatabaseError(f"Error al obtener candidatos: {str(e)}")
    
    def get_candidate_by_id(self, candidate_id: int) -> CandidateResponse:
        try:
            candidate_data = self.repository.get_by_id(candidate_id)
            if not candidate_data:
                raise CandidateNotFoundError(f"Candidato con ID {candidate_id} no encontrado")
            return self._to_response(candidate_data)
        except Exception as e:
            raise DatabaseError(f"Error al obtener candidato: {str(e)}")
    
    def update_candidate(self, candidate_id: int, update_dto: CandidateUpdate) -> CandidateResponse:
        try:
            existing = self.repository.get_by_id(candidate_id)
            if not existing:
                raise CandidateNotFoundError(f"Candidato con ID {candidate_id} no encontrado")
            
            if update_dto.email and self.repository.exists_by_email(update_dto.email):
                existing_by_email = self.repository.get_by_email(update_dto.email)
                if existing_by_email and existing_by_email[0] != candidate_id:
                    raise DuplicateEmailError(f"El email {update_dto.email} ya está registrado")
            
            if not self.repository.update(
                candidate_id,
                update_dto.name,
                update_dto.email,
                update_dto.party
            ):
                raise DatabaseError("Error al actualizar el candidato")
            
            updated_data = self.repository.get_by_id(candidate_id)
            return self._to_response(updated_data)
        except Exception as e:
            raise DatabaseError(f"Error al actualizar candidato: {str(e)}")
    
    def delete_candidate(self, candidate_id: int) -> bool:
        try:
            if not self.repository.get_by_id(candidate_id):
                raise CandidateNotFoundError(f"Candidato con ID {candidate_id} no encontrado")
            
            return self.repository.delete(candidate_id)
        except Exception as e:
            raise DatabaseError(f"Error al eliminar candidato: {str(e)}")
    
    def _to_response(self, data) -> CandidateResponse:
        if not data:
            return None
        return CandidateResponse(
            id=data[0],
            name=data[1],
            email=data[2],
            party=data[3],
            votes=data[4],
            created_at=data[5],
            updated_at=data[6] if len(data) > 6 else None
        )
    
    def close(self):
        self.repository.close()