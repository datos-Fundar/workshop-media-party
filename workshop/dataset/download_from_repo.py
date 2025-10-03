from tqdm.auto import tqdm
from workshop.utils import github
import pathlib
import urllib.request

def download_from_repo(
    from_repo: str,
    to_local: str,
) -> str:
    repo = pathlib.Path(from_repo)
    owner, repo, *dirpath = repo.parts

    local = pathlib.Path(to_local)

    if local.is_file():
        raise ValueError("local_path must be a directory")

    local.mkdir(parents=True, exist_ok=True)

    dirpath = "/".join(dirpath)

    file_list = github.list_files(owner, repo, dirpath)
    for file in tqdm(file_list):
        filename = file.get("name")
        path = local / filename

        if path.exists():
            continue

        download_url = file.get("download_url")
        urllib.request.urlretrieve(download_url, path)

    return to_local