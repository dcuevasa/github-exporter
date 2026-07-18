import base64
import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError("GITHUB_TOKEN was not found in the .env file")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
}


def get_all_repos():
    """Get all repositories for the authenticated user."""
    repos = []
    page = 1

    while True:
        url = f"https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner,collaborator"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"Error fetching repositories: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        repos.extend(data)
        page += 1

    return repos


def get_repository_readme(owner, repo_name):
    """Get the README content for a repository."""
    url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 404:
        return None

    if response.status_code != 200:
        print(f"Error fetching README for {owner}/{repo_name}: {response.status_code}")
        return None

    payload = response.json()
    content = payload.get("content")

    if not content:
        return None

    try:
        return base64.b64decode(content).decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return None


def main():
    print("Starting GitHub data export with README content...")
    raw_repos = get_all_repos()
    export_data = []

    for index, repo in enumerate(raw_repos):
        owner = repo["owner"]["login"]
        name = repo["name"]

        print(f"Processing ({index + 1}/{len(raw_repos)}): {owner}/{name}")

        repo_info = {
            "name": name,
            "full_name": repo["full_name"],
            "owner": owner,
            "private": repo["private"],
            "html_url": repo["html_url"],
            "description": repo["description"],
            "language": repo["language"],
            "created_at": repo["created_at"],
            "updated_at": repo["updated_at"],
            "readme": get_repository_readme(owner, name),
        }
        export_data.append(repo_info)

    output_file = "github_export_with_readmes.json"
    with open(output_file, "w", encoding="utf-8") as file_handle:
        json.dump(export_data, file_handle, ensure_ascii=False, indent=4)

    print(f"\nProcess completed! Data exported to {output_file}")


if __name__ == "__main__":
    main()