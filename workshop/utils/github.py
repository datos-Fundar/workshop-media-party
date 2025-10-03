import requests
import base64
from typing import Any

def get_repository(owner: str, repo: str, token: None | str = None) -> None | dict[str, Any]:
    """Get repository information."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Authorization": f"token {token}"} if token else {}
    
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None


def list_files(owner: str, repo: str, path: str = "", token: None | str = None) -> None | list[dict[str, Any]]:
    """List files and directories at the specified path."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"} if token else {}
    
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None


def get_file(owner: str, repo: str, path: str, token: None | str = None) -> None | str:
    """Get file content by path. Returns decoded content."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"} if token else {}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = response.json().get("content")
        return base64.b64decode(content).decode("utf-8") if content else None
    return None


def download_file(owner: str, repo: str, path: str, local_path: str, token: None | str = None) -> bool:
    """Download file to local path. Returns success status."""
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}"} if token else {}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        download_url = response.json().get("download_url")
        if download_url:
            file_response = requests.get(download_url)
            with open(local_path, "wb") as f:
                f.write(file_response.content)
            return True
    return False