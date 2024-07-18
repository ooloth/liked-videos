import logging
from typing import Literal

from liked_videos import log

# from liked_videos import notes
from liked_videos import youtube


log.setup_logging()  # one-time setup on startup

logger = logging.getLogger(__name__)


# TODO: run tests, linting, type checking, tests as a pre-commit hook (since committing to main)?
# TODO: persist logs somewhere? file? sqlite db? cloud logging service?
def main() -> Literal[0, 1]:
    try:
        client = youtube.create_authenticated_client()
        liked_youtube_videos = youtube.fetch_liked_videos(client)
        # TODO: fetch youtube video IDs included in my notes (reference local path to notes? assume host has no such path and temporarily clone the repo?)
        # youtube_videos_in_notes = notes.fetch_youtube_video_ids()
        # TODO: identify which liked videos are missing from my notes
        # TODO: identify which videos in my notes aren't like on YouTube? Do I want to be aware of those so I can go like them?
        # TODO: identify which videos in my notes are no longer available on YouTube? Do I want to be aware of those so I can remove them from my notes?
        # TODO: generate markdown links for each list of videos I want to add to my notes
        # TODO: append the markdown links to my inbox note (or a bots-only inbox? do I want a heading for each list of videos? with the date?)
        return 0
    except Exception as e:
        print("Unexpected error:\n", repr(e))
        return 1
