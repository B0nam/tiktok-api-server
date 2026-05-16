from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
import asyncio

from app.api.routes import (
    session,
    users,
    videos,
    search,
    trending,
    sounds,
    hashtags,
    playlists,
)
from app.api.dependencies import initialize_sessions, close_sessions
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting TikTok API Server...")
    if settings.ms_tokens and settings.ms_tokens != "YOUR_MSTOKEN_HERE":
        try:
            await asyncio.wait_for(initialize_sessions(), timeout=60)
            logger.info("Sessions auto-initialized from settings")
        except asyncio.TimeoutError:
            logger.warning("Session initialization timed out. Call /session/init manually.")
        except Exception as e:
            logger.warning(f"Could not auto-initialize sessions: {e}. Call /session/init manually.")
    else:
        logger.info("No MS_TOKENS configured. Call POST /session/init after adding your tokens to .env")

    yield

    logger.info("Shutting down TikTok API Server...")
    await close_sessions()


app = FastAPI(
    title="TikTok API Server",
    description="REST API for TikTok-Api wrapper with Swagger documentation",
    version="1.0.0",
    lifespan=lifespan,
)
from app.api.dependencies import initialize_sessions, close_sessions
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="TikTok API Server",
    description="REST API for TikTok-Api wrapper with Swagger documentation",
    version="1.0.0",
)

app.include_router(session.router)
app.include_router(users.router)
app.include_router(videos.router)
app.include_router(search.router)
app.include_router(trending.router)
app.include_router(sounds.router)
app.include_router(hashtags.router)
app.include_router(playlists.router)


@app.get("/")
async def root():
    return {
        "message": "TikTok API Server",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    from app.api.dependencies import is_session_initialized, get_session_count
    return {
        "status": "healthy",
        "sessions_initialized": is_session_initialized(),
        "session_count": get_session_count()
    }