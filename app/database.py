from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importaciones relativas
from app.api.routes import voters_router, candidates_router, votes_router

app = FastAPI(
    title="Sistema de Votación API",
    description="API REST para gestionar votaciones, votantes y candidatos",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(voters_router)
app.include_router(candidates_router)
app.include_router(votes_router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Sistema de Votación API",
        "docs": "/api/docs",
        "redoc": "/api/redoc"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}