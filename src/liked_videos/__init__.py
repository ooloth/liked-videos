import logging
from typing import Literal

from liked_videos import log
from liked_videos import youtube


log.setup_logging()  # one-time setup on startup
logger = logging.getLogger(__name__)


def main() -> Literal[0, 1]:
    try:
        client = youtube.create_authenticated_client()
        liked_videos = youtube.fetch_liked_videos(client)
        return 0
    except Exception as e:
        print(repr(e))
        return 1
