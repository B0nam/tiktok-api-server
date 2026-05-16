from fastapi import APIRouter, HTTPException, Query
from app.api.dependencies import get_api, is_session_initialized
from app.models.schemas import PaginatedResponse

router = APIRouter(prefix="/search", tags=["Search"])


def _check_session():
    if not is_session_initialized():
        raise HTTPException(status_code=400, detail="Sessions not initialized. Call /session/init first.")


@router.get("/users", response_model=PaginatedResponse)
async def search_users(
    q: str = Query(..., description="Search query"),
    count: int = Query(default=10, le=50),
    cursor: int = Query(default=0),
):
    """Search for users."""
    _check_session()
    api = await get_api()

    users = []
    async for user in api.search.users(search_term=q, count=count, cursor=cursor):
        users.append(user.as_dict)

    has_more = len(users) == count
    next_cursor = cursor + len(users)

    return PaginatedResponse(data=users, has_more=has_more, cursor=str(next_cursor))


@router.get("/videos", response_model=PaginatedResponse)
async def search_videos(
    q: str = Query(..., description="Search query"),
    count: int = Query(default=10, le=50),
    cursor: int = Query(default=0),
):
    """Search for videos."""
    _check_session()
    api = await get_api()

    videos = []
    async for video in api.search.search_type(search_term=q, obj_type="item", count=count, cursor=cursor):
        videos.append(video.as_dict)

    has_more = len(videos) == count
    next_cursor = cursor + len(videos)

    return PaginatedResponse(data=videos, has_more=has_more, cursor=str(next_cursor))