from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.api.error_handlers import register_error_handlers
from server.api.routes import analysis, jobs, projects, upload

app = FastAPI(title="System Reforge API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

app.include_router(projects.router)
app.include_router(upload.router)
app.include_router(jobs.router)
app.include_router(analysis.router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
