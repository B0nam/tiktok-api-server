from fastapi import APIRouter, HTTPException, Query
from app.api.dependencies import get_api, is_session_initialized
from app.models.schemas import SoundResponse, PaginatedResponse

router = APIRouter(prefix="/sounds", tags=["Sounds"])


def _check_session():
    if not is_session_initialized():
        raise HTTPException(status_code=400, detail="Sessions not initialized. Call /session/init first.")


@router.get("/{sound_id}", response_model=SoundResponse)
async def get_sound(sound_id: str):
    """Get sound/music information."""
    _check_session()
    api = await get_api()
    sound = api.sound(id=sound_id)
    info = await sound.info()
    return SoundResponse(data=info)


@router.get("/{sound_id}/videos", response_model=PaginatedResponse)
async def get_sound_videos(
    sound_id: str,
    count: int = Query(default=30, le=100),
    cursor: int = Query(default=0),
):
    """Get videos using this sound (paginated)."""
    _check_session()
    api = await get_api()
    sound = api.sound(id=sound_id)

    videos = []
    async for video in sound.videos(count=count, cursor=cursor):
        videos.append(video.as_dict)

    has_more = len(videos) == count
    next_cursor = cursor + len(videos)

    return PaginatedResponse(data=videos, has_more=has_more, cursor=str(next_cursor))