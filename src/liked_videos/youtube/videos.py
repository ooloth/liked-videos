from datetime import datetime

from googleapiclient.discovery import Resource
from pydantic import BaseModel, ValidationError

from liked_videos.logging import log
from liked_videos.utils import pretty_json


class YouTubeVideo(BaseModel):
    channel: str
    date: datetime
    id: str
    title: str


def _parse_youtube_videos(response: dict) -> list[YouTubeVideo]:
    videos = []

    log.debug(f"🥁 Parsing {len(response.get('items', []))} videos...")
    for item in response.get("items", []):
        try:
            video_data = {
                "channel": item["snippet"]["channelTitle"],
                "date": item["snippet"]["publishedAt"],
                "id": item["id"],
                "title": item["snippet"]["title"],
            }
            video = YouTubeVideo(**video_data)
            videos.append(video)
        except KeyError as e:
            log.error(f"😱 Missing key in video data: {e}")
        except ValidationError as e:
            log.error(f"😱 Validation error for video data: {e}")

    log.debug(f"👍 Parsed {len(videos)} videos")
    return videos


def fetch_liked_videos(client: Resource) -> list[YouTubeVideo]:
    """
    Fetches my liked videos from YouTube using a client authenticated via Oath.

    YouTube API docs: https://developers.google.com/youtube/v3/docs/videos/list
    """
    liked_videos: list[YouTubeVideo] = []
    maxResultsPerPage = 50
    nextPageToken = None  # empty for the first request

    log.info("🥁 Fetching liked videos...")
    while True:
        try:
            if nextPageToken:
                log.debug(f"🥁 Fetching up to {maxResultsPerPage} more liked videos...")

            liked_videos_request = client.videos().list(
                maxResults=maxResultsPerPage,
                myRating="like",
                pageToken=nextPageToken,  # comes from the previous request
                part="snippet",
            )

            response: dict = liked_videos_request.execute()
            log.debug(f"🔍 Liked videos response:\n{pretty_json(response)}")
            # TODO: increase logging detail to capture the pageInfo and items count for each request. This can help identify if any requests are returning fewer items than expected.

            new_videos = _parse_youtube_videos(response)
            log.debug(f"👍 Fetched {len(new_videos)} new liked videos")

            liked_videos.extend(_parse_youtube_videos(response))

            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:
                break
        except Exception as e:
            log.error(f"😱 Error fetching liked videos: {e}")
            raise

    log.info(f"👍 Fetched {len(liked_videos)} liked videos")
    return liked_videos
