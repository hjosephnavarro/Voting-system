from app.api.routes.voters import router as voters_router
from app.api.routes.candidates import router as candidates_router
from app.api.routes.votes import router as votes_router

__all__ = ['voters_router', 'candidates_router', 'votes_router']