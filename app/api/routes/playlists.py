from fastapi import APIRouter, HTTPException, Query
from app.api.dependencies import get_api, is_session_initialized
from app.models.schemas import PlaylistResponse, PaginatedResponse

router = APIRouter(prefix="/playlists", tags=["Playlists"])


def _check_session():
    if not is_session_initialized():
        raise HTTPException(status_code=400, detail="Sessions not initialized. Call /session/init first.")


@router.get("/{playlist_id}", response_model=PlaylistResponse)
async def get_playlist(playlist_id: str):
    """Get playlist information."""
    _check_session()
    api = await get_api()
    playlist = api.playlist(id=playlist_id)
    info = await playlist.info()
    return PlaylistResponse(data=info)


@router.get("/{playlist_id}/videos", response_model=PaginatedResponse)
async def get_playlist_videos(
    playlist_id: str,
    count: int = Query(default=30, le=100),
    cursor: int = Query(default=0),
):
    """Get videos in playlist (paginated)."""
    _check_session()
    api = await get_api()
    playlist = api.playlist(id=playlist_id)

    videos = []
    async for video in playlist.videos(count=count, cursor=cursor):
        videos.append(video.as_dict)

    has_more = len(videos) == count
    next_cursor = cursor + len(videos)

    return PaginatedResponse(data=videos, has_more=has_more, cursor=str(next_cursor))