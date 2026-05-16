from fastapi import APIRouter, HTTPException
from app.api.dependencies import (
    initialize_sessions,
    close_sessions,
    is_session_initialized,
    get_session_count,
)
from app.models.schemas import SessionStatus

router = APIRouter(prefix="/session", tags=["Session"])


@router.get("/status", response_model=SessionStatus)
async def get_session_status():
    """Check the status of TikTok sessions."""
    return SessionStatus(
        initialized=is_session_initialized(),
        session_count=get_session_count(),
    )


@router.post("/init")
async def init_session():
    """Initialize TikTok sessions."""
    import asyncio
    try:
        await asyncio.wait_for(initialize_sessions(), timeout=120)
        return {"message": "Sessions initialized successfully", "session_count": get_session_count()}
    except asyncio.TimeoutError:
        raise HTTPException(status_code=500, detail="Session initialization timed out after 120s")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize sessions: {str(e)}")


@router.post("/close")
async def close_session():
    """Close TikTok sessions."""
    await close_sessions()
    return {"message": "Sessions closed successfully"}