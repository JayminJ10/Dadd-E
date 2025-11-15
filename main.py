"""
Dadd-E Entry Point
Run this to start the FastAPI backend server
"""
import uvicorn
from app.core.config import get_settings


def main() -> None:
    """Start the Dadd-E backend server"""
    settings = get_settings()

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
