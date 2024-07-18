from datetime import datetime
import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from pydantic import BaseModel, ValidationError

from liked_videos.utils import pretty_json, pretty_print_json

logger = logging.getLogger(__name__)


API_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
OATH_CLIENT_SECRETS_FILE = ".secrets/oath_client_secrets.json"
OATH_TOKENS_FILE = ".secrets/oath_tokens.json"


def _fetch_new_oauth_tokens(
    client_secrets: str = OATH_CLIENT_SECRETS_FILE,
    scopes: list[str] = API_SCOPES,
) -> Credentials:
    """
    Fetches new Google Cloud OAuth tokens using client secrets file.

    OAuth client: https://console.cloud.google.com/apis/credentials?project=michael-uloth
    """
    logger.info("Fetching new tokens")

    try:
        flow = InstalledAppFlow.from_client_secrets_file(client_secrets, scopes)
        credentials = flow.run_local_server()
        return credentials
    except FileNotFoundError as e:
        logger.error(f"OAuth client secrets file not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while fetching new OAuth tokens: {e}")
        raise


def _generate_oauth_credentials(tokens: str = OATH_TOKENS_FILE) -> Credentials:
    """
    Generates OAuth credentials from a Google Cloud client secrets file.

    OAuth client: https://console.cloud.google.com/apis/credentials?project=michael-uloth
    """
    credentials = None

    logger.info("Checking for saved tokens")

    if os.path.exists(tokens):
        logger.info("Saved tokens found")
        try:
            logger.info(f"Loading saved tokens from {tokens}")
            credentials = Credentials.from_authorized_user_file(tokens)
        except Exception as e:
            logger.info(f"Error loading tokens: {e}")
            credentials = _fetch_new_oauth_tokens()
    else:
        logger.info("No saved tokens found")

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                logger.info("Refreshing expired access token")
                credentials.refresh(Request())
            except Exception as e:
                logger.info(f"Error refreshing token: {e}")
                credentials = _fetch_new_oauth_tokens()
        else:
            credentials = _fetch_new_oauth_tokens()

        logger.info(f"Saving updated tokens to {tokens}")
        with open(tokens, "w") as file:
            file.write(credentials.to_json())

    return credentials


def create_authenticated_client() -> Resource:
    """
    Creates an authenticated client to interact with the YouTube API.

    Corey Shafer tutorial: https://www.youtube.com/watch?v=vQQEaSnQ_bs
    Martin Heinz tutorial: https://martinheinz.dev/blog/84
    YouTube API docs: https://developers.google.com/youtube/v3/quickstart/python
    """
    credentials = _generate_oauth_credentials()
    return build(credentials=credentials, serviceName="youtube", version="v3")


class YouTubeVideo(BaseModel):
    channel: str
    date: datetime
    id: str
    title: str


def _parse_youtube_videos(response: dict) -> list[YouTubeVideo]:
    videos = []

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
            logger.error(f"Missing key in video data: {e}")
        except ValidationError as e:
            logger.error(f"Validation error for video data: {e}")

    return videos


def fetch_liked_videos(client: Resource) -> list[YouTubeVideo]:
    """
    Fetches my liked videos from YouTube using a client authenticated via Oath.

    YouTube API docs: https://developers.google.com/youtube/v3/docs/videos/list
    """
    liked_videos: list[YouTubeVideo] = []
    maxResultsPerPage = 50
    nextPageToken = None  # empty for the first request

    while True:
        try:
            logger.info(f"Fetching next {maxResultsPerPage} liked videos")

            liked_videos_request = client.videos().list(
                maxResults=maxResultsPerPage,
                myRating="like",
                pageToken=nextPageToken,  # comes from the previous request
                part="snippet",
            )

            response: dict = liked_videos_request.execute()
            logger.debug(f"Liked videos response:\n{pretty_json(response)}")

            new_videos = _parse_youtube_videos(response)
            logger.debug(f"Found {len(new_videos)} new liked videos")

            liked_videos.extend(_parse_youtube_videos(response))

            nextPageToken = response.get("nextPageToken")
            if not nextPageToken:
                break
        except Exception as e:
            logger.error(f"Error fetching liked videos: {e}")
            raise

    logger.info(f"Found {len(liked_videos)} liked videos")
    return liked_videos
