from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os
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

# Servir archivos estáticos
base_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(base_dir, "static")

print(f" Base dir: {base_dir}")
print(f" Static dir: {static_dir}")
print(f" Static exists: {os.path.exists(static_dir)}")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    print("✅ Static files mounted")
else:
    print("❌ Static directory not found")

app.include_router(voters_router)
app.include_router(candidates_router)
app.include_router(votes_router)

@app.get("/", tags=["Root"])
async def root():
    index_path = os.path.join(static_dir, "index.html")
    print(f" Index path: {index_path}")
    print(f" Index exists: {os.path.exists(index_path)}")
    
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        return HTMLResponse("""
        <html>
            <head><title>Sistema de Votación</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                <div style="background: white; padding: 40px; border-radius: 20px; max-width: 600px; margin: 0 auto; box-shadow: 0 20px 60px rgba(0,0,0,0.3);">
                    <h1 style="color: #333;">🗳️ Sistema de Votación</h1>
                    <p style="color: #666; font-size: 18px; margin: 20px 0;">La API está funcionando correctamente</p>
                    <p style="color: #999;">Pero el archivo index.html no se encuentra en <br><code style="background: #f0f0f0; padding: 5px 10px; border-radius: 5px;">app/static/index.html</code></p>
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #eee;">
                        <a href="/api/docs" style="color: #667eea; text-decoration: none; font-weight: 600; margin: 0 15px;">📚 Documentación</a>
                        <a href="/health" style="color: #667eea; text-decoration: none; font-weight: 600; margin: 0 15px;">❤️ Health Check</a>
                    </div>
                </div>
            </body>
        </html>
        """)

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}