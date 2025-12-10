import requests
from zipfile import ZipFile
import io
from pathlib import Path
from typing import Iterable
import shutil
import sys

def github_releases(repo: str) -> dict:
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"

    try:
        releases = try_get(api_url).json()
    except requests.HTTPError as e:
        fatal_error(f"GitHub API request failed: {e}")

    return releases

def download_zip(download_url: str) -> ZipFile:
    try:
        zip_ref = ZipFile(
            io.BytesIO(
                try_get(download_url).content
            )
        )
    except requests.HTTPError as e:
        fatal_error(f"Font download failed: {e}")

    return zip_ref

def save_members(zip_ref: ZipFile, out_dir: Path, *members: str):
    """
    Extract zip members without their parent directories.
    out_dir path must be valid.
    Non-unique filenames will be overwritten.
    """

    for member in members:
        dest_path = Path(
            out_dir,
            Path(member).name
        )
        with zip_ref.open(member) as source, open(dest_path, "wb") as destination:
            shutil.copyfileobj(source, destination)

def try_get(url: str) -> requests.Response:
    response = requests.get(url)
    response.raise_for_status()
    return response

def fatal_error(message: str):
    """Print to stderr and exit"""

    print(message, file=sys.stderr)
    sys.exit(1)
