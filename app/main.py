"""
Dadd-E FastAPI Application
Main entry point for the productivity assistant backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.routers import voice, vision, actions

# Get settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Real-time productivity assistant using Omi glasses",
    version="0.1.0",
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(voice.router)
app.include_router(vision.router)
app.include_router(actions.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint"""
    return {
        "app": settings.app_name,
        "version": "0.1.0",
        "status": "running",
    }


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.app_name,
    }


@app.on_event("startup")
async def startup_event() -> None:
    """Startup event handler"""
    print(f"🚀 Starting {settings.app_name}")
    print(f"📡 Wake word: {settings.wake_word}")
    print(f"🔧 Debug mode: {settings.debug}")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Shutdown event handler"""
    print(f"👋 Shutting down {settings.app_name}")
