from app.repositories.voter_repository import VoterRepository
from app.schemas.voter import VoterCreate, VoterUpdate, VoterResponse
from app.exceptions.custom_exceptions import DuplicateEmailError, VoterNotFoundError, DatabaseError

class VoterService:
    def __init__(self):
        self.repository = VoterRepository()
    
    def create_voter(self, create_dto: VoterCreate) -> VoterResponse:
        try:
            if self.repository.exists_by_email(create_dto.email):
                raise DuplicateEmailError(f"El email {create_dto.email} ya está registrado")
            
            voter_id = self.repository.create(create_dto.name, create_dto.email)
            if not voter_id:
                raise DatabaseError("Error al crear el votante")
            
            voter_data = self.repository.get_by_id(voter_id)
            return self._to_response(voter_data)
        except Exception as e:
            raise DatabaseError(f"Error al crear votante: {str(e)}")
    
    def get_all_voters(self) -> list[VoterResponse]:
        try:
            voters_data = self.repository.get_all()
            return [self._to_response(data) for data in voters_data]
        except Exception as e:
            raise DatabaseError(f"Error al obtener votantes: {str(e)}")
    
    def get_voter_by_id(self, voter_id: int) -> VoterResponse:
        try:
            voter_data = self.repository.get_by_id(voter_id)
            if not voter_data:
                raise VoterNotFoundError(f"Votante con ID {voter_id} no encontrado")
            return self._to_response(voter_data)
        except Exception as e:
            raise DatabaseError(f"Error al obtener votante: {str(e)}")
    
    def update_voter(self, voter_id: int, update_dto: VoterUpdate) -> VoterResponse:
        try:
            existing = self.repository.get_by_id(voter_id)
            if not existing:
                raise VoterNotFoundError(f"Votante con ID {voter_id} no encontrado")
            
            if update_dto.email and self.repository.exists_by_email(update_dto.email):
                existing_by_email = self.repository.get_by_email(update_dto.email)
                if existing_by_email and existing_by_email[0] != voter_id:
                    raise DuplicateEmailError(f"El email {update_dto.email} ya está registrado")
            
            name = update_dto.name if update_dto.name is not None else existing[1]
            email = update_dto.email if update_dto.email is not None else existing[2]
            
            if not self.repository.update(voter_id, name, email):
                raise DatabaseError("Error al actualizar el votante")
            
            updated_data = self.repository.get_by_id(voter_id)
            return self._to_response(updated_data)
        except Exception as e:
            raise DatabaseError(f"Error al actualizar votante: {str(e)}")
    
    def delete_voter(self, voter_id: int) -> bool:
        try:
            if not self.repository.get_by_id(voter_id):
                raise VoterNotFoundError(f"Votante con ID {voter_id} no encontrado")
            
            return self.repository.delete(voter_id)
        except Exception as e:
            raise DatabaseError(f"Error al eliminar votante: {str(e)}")
    
    def get_available_voters(self) -> list[dict]:
        try:
            return self.repository.get_available_voters()
        except Exception as e:
            raise DatabaseError(f"Error al obtener votantes disponibles: {str(e)}")
    
    def _to_response(self, data) -> VoterResponse:
        if not data:
            return None
        return VoterResponse(
            id=data[0],
            name=data[1],
            email=data[2],
            has_voted=data[3],
            created_at=data[4],
            updated_at=data[5] if len(data) > 5 else None
        )
    
    def close(self):
        self.repository.close()