from fastapi import APIRouter, HTTPException, Query
from app.api.dependencies import get_api, is_session_initialized
from app.models.schemas import PaginatedResponse

router = APIRouter(prefix="/trending", tags=["Trending"])


def _check_session():
    if not is_session_initialized():
        raise HTTPException(status_code=400, detail="Sessions not initialized. Call /session/init first.")


@router.get("", response_model=PaginatedResponse)
async def get_trending(
    count: int = Query(default=30, le=100),
):
    """Get trending videos."""
    _check_session()
    api = await get_api()

    videos = []
    async for video in api.trending.videos(count=count):
        videos.append(video.as_dict)

    return PaginatedResponse(data=videos, has_more=False)