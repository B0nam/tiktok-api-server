from pydantic import BaseModel
from typing import Optional, Any


class UserInfo(BaseModel):
    user_id: Optional[str] = None
    sec_uid: Optional[str] = None
    username: Optional[str] = None
    avatar: Optional[str] = None
    bio: Optional[str] = None
    following_count: Optional[int] = None
    follower_count: Optional[int] = None
    likes_count: Optional[int] = None
    is_verified: Optional[bool] = None


class UserResponse(BaseModel):
    data: UserInfo


class VideoInfo(BaseModel):
    id: Optional[str] = None
    description: Optional[str] = None
    create_time: Optional[str] = None
    author: Optional[dict] = None
    sound: Optional[dict] = None
    stats: Optional[dict] = None
    hashtags: Optional[list] = None


class VideoResponse(BaseModel):
    data: VideoInfo


class CommentInfo(BaseModel):
    id: Optional[str] = None
    text: Optional[str] = None
    author: Optional[dict] = None
    likes_count: Optional[int] = None
    create_time: Optional[int] = None


class PaginatedResponse(BaseModel):
    data: list[Any]
    has_more: bool
    cursor: Optional[str] = None


class SearchUserResponse(BaseModel):
    data: list[dict]
    has_more: bool = False
    cursor: Optional[str] = None


class TrendingResponse(BaseModel):
    data: list[dict]
    has_more: bool = False


class SoundInfo(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    author: Optional[dict] = None
    duration: Optional[int] = None
    original: Optional[bool] = None


class SoundResponse(BaseModel):
    data: SoundInfo


class HashtagInfo(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    video_count: Optional[int] = None


class HashtagResponse(BaseModel):
    data: HashtagInfo


class PlaylistInfo(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    video_count: Optional[int] = None
    cover_url: Optional[str] = None
    creator: Optional[dict] = None


class PlaylistResponse(BaseModel):
    data: PlaylistInfo


class SessionStatus(BaseModel):
    initialized: bool
    session_count: int


class ErrorResponse(BaseModel):
    detail: str