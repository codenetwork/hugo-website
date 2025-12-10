import requests
from zipfile import ZipFile
import io
from pathlib import Path
from typing import Iterable, BinaryIO
import shutil
import sys
from fontTools.ttLib import TTFont
import fontTools.ttLib.woff2

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

def to_woff2(source: BinaryIO, dest_path: Path):
    font = TTFont(source)
    font.flavor = "woff2"
    font.save(dest_path)

def save_members(zip_ref: ZipFile, out_dir: Path, *members: str):
    """
    Extract zip members without their parent directories.
    out_dir path must be valid.
    Non-unique filenames will be overwritten.
    """

    for member in members:
        member_path = Path(member)

        dest_filename = member_path.name
        is_ttf = member_path.suffix in (".ttf", ".otf")

        if is_ttf:
            dest_filename = member_path.stem + ".woff2"

        dest_path = Path(
            out_dir,
            dest_filename
        )
        with zip_ref.open(member) as source:
            if is_ttf:
                to_woff2(source, dest_path)
            else:
                with open(dest_path, "wb") as destination:
                    shutil.copyfileobj(source, destination)

def try_get(url: str) -> requests.Response:
    response = requests.get(url)
    response.raise_for_status()
    return response

def fatal_error(message: str):
    """Print to stderr and exit"""

    print(message, file=sys.stderr)
    sys.exit(1)
