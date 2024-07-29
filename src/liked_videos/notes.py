from dotenv import load_dotenv
import git
from git.types import PathLike
import os

from liked_videos.logging import log

load_dotenv()

LOCAL_REPO_PATH = os.getenv("LOCAL_REPO_PATH") or ""
REMOTE_REPO_PATH = os.getenv("REMOTE_REPO_PATH") or ""
INBOX_FILE_PATH = os.getenv("INBOX_FILE_PATH") or ""


def get_local_repo(
    local_repo_path: PathLike = LOCAL_REPO_PATH,
    remote_repo_path: PathLike = REMOTE_REPO_PATH,
) -> git.Repo:
    if not os.path.isdir(local_repo_path):
        repo = git.Repo.clone_from(remote_repo_path, local_repo_path)
    else:
        repo = git.Repo(local_repo_path)

    if repo.active_branch.name != "main":
        log.warning("not on main branch; switching to main")
        # FIXME: THIS IS COMMITTING TO THIS REPO INSTEAD OF CONTENT!
        repo.index.commit("committing local changes")
        repo.git.checkout("main")

    if repo.is_dirty():
        log.warning("repo is dirty; committing local changes before pulling")
        repo.index.commit("committing local changes before")
        assert not repo.is_dirty()

    repo.remotes.origin.pull()

    return repo


def fetch_youtube_video_ids() -> list[str]:
    repo = get_local_repo()

    with open(INBOX_FILE_PATH, "r") as f:
        lines = f.readlines()
        print("lines", lines)

    return []
