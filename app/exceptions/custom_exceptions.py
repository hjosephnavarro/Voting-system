class VotingSystemError(Exception):
    """Excepción base del sistema de votación"""
    pass

class DuplicateEmailError(VotingSystemError):
    """Error cuando un email ya está registrado"""
    pass

class VoterNotFoundError(VotingSystemError):
    """Error cuando no se encuentra un votante"""
    pass

class CandidateNotFoundError(VotingSystemError):
    """Error cuando no se encuentra un candidato"""
    pass

class VoteNotFoundError(VotingSystemError):
    """Error cuando no se encuentra un voto"""
    pass

class VoterAlreadyVotedError(VotingSystemError):
    """Error cuando un votante ya emitió su voto"""
    pass

class InvalidVoterError(VotingSystemError):
    """Error cuando el votante no es válido"""
    pass

class InvalidCandidateError(VotingSystemError):
    """Error cuando el candidato no es válido"""
    pass

class DatabaseError(VotingSystemError):
    """Error en la base de datos"""
    pass