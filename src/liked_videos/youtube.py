# see: https://developers.google.com/youtube/v3/quickstart/python
# see: https://developers.google.com/youtube/v3/docs/videos/list
# see: https://www.youtube.com/watch?v=vQQEaSnQ_bs


# import os

from google.auth.external_account_authorized_user import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource

# from liked_videos.utils import pretty_print_json


OATH_CLIENT_SECRETS = ".secrets/oath_client_secrets.json"
API_SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def _generate_oauth_credentials_from_secrets_file(
    client_secrets: str = OATH_CLIENT_SECRETS,
    scopes: list[str] = API_SCOPES,
) -> Credentials:
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=client_secrets,
        scopes=scopes,
    )

    credentials = flow.run_local_server()

    return credentials


def create_authenticated_client() -> Resource:
    credentials = _generate_oauth_credentials_from_secrets_file()
    return build(credentials=credentials, serviceName="youtube", version="v3")


# TODO: improve return type
def fetch_liked_videos(client: Resource) -> list[dict]:
    request = client.videos().list(
        myRating="like",
        part="snippet,contentDetails,statistics",
    )

    response: dict = request.execute()
    # pretty_print_json(response)

    return response["items"]
