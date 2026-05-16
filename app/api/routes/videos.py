from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from app.api.dependencies import get_api, is_session_initialized
from app.models.schemas import VideoResponse, PaginatedResponse
from typing import Optional, AsyncIterator

router = APIRouter(prefix="/videos", tags=["Videos"])


def _check_session():
    if not is_session_initialized():
        raise HTTPException(status_code=400, detail="Sessions not initialized. Call /session/init first.")


@router.get("/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str):
    """Get video metadata."""
    _check_session()
    api = await get_api()
    video_url = f"https://www.tiktok.com/@user/video/{video_id}"
    video = api.video(id=video_id, url=video_url)
    info = await video.info()
    return VideoResponse(data=info)


@router.get("/{video_id}/comments", response_model=PaginatedResponse)
async def get_video_comments(
    video_id: str,
    count: int = Query(default=20, le=50),
    cursor: int = Query(default=0),
):
    """Get video comments (paginated)."""
    _check_session()
    api = await get_api()
    video = api.video(id=video_id)

    comments = []
    async for comment in video.comments(count=count, cursor=cursor):
        comments.append(comment.as_dict)

    has_more = len(comments) == count
    next_cursor = cursor + len(comments)

    return PaginatedResponse(data=comments, has_more=has_more, cursor=str(next_cursor))


@router.get("/{video_id}/related", response_model=PaginatedResponse)
async def get_related_videos(
    video_id: str,
    count: int = Query(default=30, le=50),
):
    """Get related videos."""
    _check_session()
    api = await get_api()
    video = api.video(id=video_id)

    videos = []
    async for related in video.related_videos(count=count):
        videos.append(related.as_dict)

    return PaginatedResponse(data=videos, has_more=False)


@router.get("/{video_id}/download")
async def download_video(video_id: str):
    """Download video file."""
    _check_session()
    api = await get_api()
    video = api.video(id=video_id)
    await video.info()

    video_bytes = await video.bytes()

    async def video_stream():
        if hasattr(video_bytes, '__aiter__'):
            async for chunk in video_bytes:
                yield chunk
        else:
            yield video_bytes

    return StreamingResponse(
        video_stream(),
        media_type="video/mp4",
        headers={
            "Content-Disposition": f"attachment; filename={video_id}.mp4"
        }
    )