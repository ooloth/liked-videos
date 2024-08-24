from typing import Literal

from liked_videos import notes
from liked_videos.logging import configure_logger, log

# from liked_videos import notes
from liked_videos.youtube import client as yt
from liked_videos.youtube.videos import fetch_liked_videos


configure_logger()  # one-time setup on startup


# TODO: run tests, linting, type checking, tests as a pre-commit hook (since committing to main)?
# TODO: persist logs somewhere? file? sqlite db? cloud logging service?
def main() -> Literal[0, 1]:
    try:
        # liked_videos = fetch_liked_videos(yt.create_authenticated_client())
        # TODO: fetch youtube videos in my notes (reference local path to notes? assume host has no such path and temporarily clone the repo?)
        youtube_videos_in_notes = notes.fetch_youtube_video_ids()
        # TODO: identify which liked videos are missing from my notes
        # TODO: identify which videos in my notes aren't like on YouTube? Do I want to be aware of those so I can go like them?
        # TODO: identify which videos in my notes are no longer available on YouTube? Do I want to be aware of those so I can remove them from my notes?
        # TODO: generate markdown links for each list of videos I want to add to my notes
        # TODO: append the markdown links to my inbox note (or a bots-only inbox? do I want a heading for each list of videos? with the date?)
        return 0
    except Exception as e:
        log.error(f"😱 Unexpected error:{e}")
        return 1
