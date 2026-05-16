from fastapi import APIRouter, HTTPException, Query
from app.api.dependencies import get_api, is_session_initialized
from app.models.schemas import UserResponse, PaginatedResponse, PlaylistResponse
from typing import Optional

router = APIRouter(prefix="/users", tags=["Users"])


def _check_session():
    if not is_session_initialized():
        raise HTTPException(status_code=400, detail="Sessions not initialized. Call /session/init first.")


@router.get("/{username}")
async def get_user(username: str):
    """Get user profile information."""
    _check_session()
    api = await get_api()
    user = api.user(username=username)
    info = await user.info()
    return info


@router.get("/{username}/videos", response_model=PaginatedResponse)
async def get_user_videos(
    username: str,
    count: int = Query(default=30, le=100),
    cursor: int = Query(default=0),
):
    """Get user's videos (paginated)."""
    _check_session()
    api = await get_api()
    user = api.user(username=username)

    videos = []
    has_more = False
    next_cursor = cursor

    async for video in user.videos(count=count, cursor=cursor):
        videos.append(video.as_dict)

    if videos:
        next_cursor = cursor + len(videos)
        has_more = len(videos) == count

    return PaginatedResponse(data=videos, has_more=has_more, cursor=str(next_cursor))


@router.get("/{username}/liked", response_model=PaginatedResponse)
async def get_user_liked(
    username: str,
    count: int = Query(default=30, le=100),
    cursor: int = Query(default=0),
):
    """Get user's liked videos (paginated)."""
    _check_session()
    api = await get_api()
    user = api.user(username=username)

    videos = []
    async for video in user.liked(count=count, cursor=cursor):
        videos.append(video.as_dict)

    has_more = len(videos) == count
    next_cursor = cursor + len(videos)

    return PaginatedResponse(data=videos, has_more=has_more, cursor=str(next_cursor))


@router.get("/{username}/playlists", response_model=PaginatedResponse)
async def get_user_playlists(
    username: str,
    count: int = Query(default=20, le=50),
    cursor: int = Query(default=0),
):
    """Get user's playlists (paginated)."""
    _check_session()
    api = await get_api()
    user = api.user(username=username)

    playlists = []
    async for playlist in user.playlists(count=count, cursor=cursor):
        playlists.append(playlist.as_dict)

    has_more = len(playlists) == count
    next_cursor = cursor + len(playlists)

    return PaginatedResponse(data=playlists, has_more=has_more, cursor=str(next_cursor))