from fontslib import *
import paths

FONTS_PATH = Path(paths.PROJECT_ROOT, "static", "fonts")

def github_zip(repo: str):
    """
    This function assumes a zip file containing the fonts is the first asset
    """

    return download_zip(
        github_releases(repo)["assets"][0]["browser_download_url"]
    )

def github_font(repo: str, *members: str):
    save_members(
        github_zip(repo),
        FONTS_PATH,
        *members
    )

def gh_namelist(repo: str):
    """
    Print the members of the zip file
    """
    print(
        github_zip(repo).namelist()
    )

def inter_format(name: str) -> str:
    return f"web/{name}.woff2"

def main():
    github_font("rsms/inter", *map(inter_format, [
        "InterVariable",
        "InterVariable-Italic",
    ]))

    github_font("djrrb/Bungee", "Bungee-fonts/Bungee_Basic/Bungee-Regular.ttf")

if __name__ == "__main__":
    main()
