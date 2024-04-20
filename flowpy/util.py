from pathlib import Path
import requests


def download_file_from_github(
    dest_file: Path,
    relative_file_path: str,
    repository="flowy-code/flowy",
    branch="main",
):
    if not dest_file.exists():
        url = f"https://raw.githubusercontent.com/{repository}/{branch}/{relative_file_path}"
        resp = requests.get(url)

        dest_file.parent.mkdir(exist_ok=True, parents=True)

        with open(dest_file, "w") as f:
            f.write(resp.text)
    else:
        print(f"{dest_file} already exists.")
