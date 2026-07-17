from app.repositories.vote_repository import VoteRepository
from app.repositories.voter_repository import VoterRepository
from app.repositories.candidate_repository import CandidateRepository
from app.schemas.vote import VoteCreate, VoteResponse, VoteDetailResponse, VoteStatisticsResponse, CandidateResult
from app.exceptions.custom_exceptions import (
    VoterNotFoundError, CandidateNotFoundError, 
    VoterAlreadyVotedError, DatabaseError
)

class VoteService:
    def __init__(self):
        self.repository = VoteRepository()
        self.voter_repository = VoterRepository()
        self.candidate_repository = CandidateRepository()
    
    def create_vote(self, create_dto: VoteCreate) -> VoteResponse:
        try:
            voter = self.voter_repository.get_by_id(create_dto.voter_id)
            if not voter:
                raise VoterNotFoundError(f"Votante con ID {create_dto.voter_id} no encontrado")
            
            if voter[3]:
                raise VoterAlreadyVotedError(f"El votante {voter[1]} ya emitió su voto")
            
            candidate = self.candidate_repository.get_by_id(create_dto.candidate_id)
            if not candidate:
                raise CandidateNotFoundError(f"Candidato con ID {create_dto.candidate_id} no encontrado")
            
            vote_id = self.repository.create(create_dto.voter_id, create_dto.candidate_id)
            if not vote_id:
                raise DatabaseError("Error al registrar el voto")
            
            return VoteResponse(
                id=vote_id,
                voter_id=create_dto.voter_id,
                candidate_id=create_dto.candidate_id,
                created_at=None
            )
        except Exception as e:
            raise DatabaseError(f"Error al registrar voto: {str(e)}")
    
    def get_all_votes(self) -> list[VoteDetailResponse]:
        try:
            votes_data = self.repository.get_all()
            return [
                VoteDetailResponse(
                    id=data[0],
                    voter_name=data[1],
                    voter_email=data[2],
                    candidate_name=data[3],
                    candidate_party=data[4],
                    created_at=data[5]
                )
                for data in votes_data
            ]
        except Exception as e:
            raise DatabaseError(f"Error al obtener votos: {str(e)}")
    
    def get_vote_by_id(self, vote_id: int) -> VoteDetailResponse:
        try:
            vote_data = self.repository.get_by_id(vote_id)
            if not vote_data:
                raise DatabaseError(f"Voto con ID {vote_id} no encontrado")
            
            return VoteDetailResponse(
                id=vote_data[0],
                voter_name=vote_data[1],
                voter_email=vote_data[2],
                candidate_name=vote_data[3],
                candidate_party=vote_data[4],
                created_at=vote_data[5]
            )
        except Exception as e:
            raise DatabaseError(f"Error al obtener voto: {str(e)}")
    
    def delete_vote(self, vote_id: int) -> bool:
        try:
            if not self.repository.get_by_id(vote_id):
                raise DatabaseError(f"Voto con ID {vote_id} no encontrado")
            
            return self.repository.delete(vote_id)
        except Exception as e:
            raise DatabaseError(f"Error al eliminar voto: {str(e)}")
    
    def get_statistics(self) -> VoteStatisticsResponse:
        try:
            total_voters = self.voter_repository.count()
            total_voted = self.voter_repository.count_voted()
            total_candidates = self.candidate_repository.count()
            total_votes = self.repository.count()
            results_data = self.repository.get_statistics()
            
            results = [
                CandidateResult(
                    candidate_id=data[0],
                    candidate_name=data[1],
                    party=data[2],
                    votes=data[3],
                    percentage=data[4]
                )
                for data in results_data
            ]
            
            return VoteStatisticsResponse(
                total_voters=total_voters,
                total_voted=total_voted,
                total_candidates=total_candidates,
                total_votes=total_votes,
                results=results
            )
        except Exception as e:
            raise DatabaseError(f"Error al obtener estadísticas: {str(e)}")
    
    def close(self):
        self.repository.close()
        self.voter_repository.close()
        self.candidate_repository.close()