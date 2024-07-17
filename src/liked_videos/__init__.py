from typing import Literal

from liked_videos import youtube
from liked_videos.utils import pretty_print_json


def main() -> Literal[0, 1]:
    try:
        client = youtube.create_authenticated_client()
        liked_videos = youtube.fetch_liked_videos(client)
        pretty_print_json(liked_videos)
        return 0
    except Exception as e:
        print(repr(e))
        return 1
