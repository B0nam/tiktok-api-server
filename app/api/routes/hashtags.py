from fastapi import APIRouter, HTTPException, Query
from app.api.dependencies import get_api, is_session_initialized
from app.models.schemas import HashtagResponse, PaginatedResponse

router = APIRouter(prefix="/hashtags", tags=["Hashtags"])


def _check_session():
    if not is_session_initialized():
        raise HTTPException(status_code=400, detail="Sessions not initialized. Call /session/init first.")


@router.get("/{hashtag}", response_model=HashtagResponse)
async def get_hashtag(hashtag: str):
    """Get hashtag/challenge information."""
    _check_session()
    api = await get_api()
    tag = api.hashtag(name=hashtag)
    info = await tag.info()
    return HashtagResponse(data=info)


@router.get("/{hashtag}/videos", response_model=PaginatedResponse)
async def get_hashtag_videos(
    hashtag: str,
    count: int = Query(default=30, le=100),
    cursor: int = Query(default=0),
):
    """Get videos with this hashtag (paginated)."""
    _check_session()
    api = await get_api()
    tag = api.hashtag(name=hashtag)

    videos = []
    async for video in tag.videos(count=count, cursor=cursor):
        videos.append(video.as_dict)

    has_more = len(videos) == count
    next_cursor = cursor + len(videos)

    return PaginatedResponse(data=videos, has_more=has_more, cursor=str(next_cursor))