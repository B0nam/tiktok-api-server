from typing import Optional
from TikTokApi import TikTokApi
from app.core.config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)

_api_instance: Optional[TikTokApi] = None
_session_initialized = False


async def get_api() -> TikTokApi:
    global _api_instance
    if _api_instance is None:
        _api_instance = TikTokApi()
    return _api_instance


async def initialize_sessions():
    global _session_initialized, _api_instance
    if _api_instance is None:
        _api_instance = TikTokApi()

    ms_tokens_list = [t.strip() for t in settings.ms_tokens.split(",") if t.strip()]

    proxies = None
    if settings.proxy:
        proxies = [settings.proxy]

    await _api_instance.create_sessions(
        num_sessions=settings.num_sessions,
        ms_tokens=ms_tokens_list if ms_tokens_list else None,
        proxies=proxies,
        headless=settings.headless,
        timeout=60000,
        allow_partial_sessions=True,
        min_sessions=1,
    )
    _session_initialized = True
    logger.info(f"Initialized {len(_api_instance.sessions)} TikTok sessions")


async def close_sessions():
    global _session_initialized, _api_instance
    if _api_instance is not None:
        await _api_instance.close_sessions()
        _session_initialized = False
        logger.info("Closed TikTok sessions")


def is_session_initialized() -> bool:
    return _session_initialized


def get_session_count() -> int:
    if _api_instance is not None:
        return len(_api_instance.sessions)
    return 0