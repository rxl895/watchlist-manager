from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import uvicorn

from app.database import SessionLocal, engine, init_db
from app.models import content as content_models
from app.routes import content, watches, ai, stats
from app.config import settings

# Initialize database
init_db()

app = FastAPI(
    title="Watchlist Manager API",
    description="A modern API for managing your movie and TV show watchlist with AI-powered features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(content.router, prefix="/api/v1", tags=["content"])
app.include_router(watches.router, prefix="/api/v1", tags=["watches"])
app.include_router(ai.router, prefix="/api/v1", tags=["ai"])
app.include_router(stats.router, prefix="/api/v1", tags=["statistics"])

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Watchlist Manager API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
