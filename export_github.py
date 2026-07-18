import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

if not TOKEN:
    raise ValueError("GITHUB_TOKEN was not found in the .env file")

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
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

def main():
    print("Starting GitHub data export...")
    raw_repos = get_all_repos()
    export_data = []

    for index, repo in enumerate(raw_repos):
        owner = repo['owner']['login']
        name = repo['name']
        
        print(f"Processing ({index + 1}/{len(raw_repos)}): {owner}/{name}")
        
        repo_info = {
            "name": name,
            "full_name": repo['full_name'],
            "owner": owner,
            "private": repo['private'],
            "html_url": repo['html_url'],
            "description": repo['description'],
            "language": repo['language'],
            "created_at": repo['created_at'],
            "updated_at": repo['updated_at']
        }
        export_data.append(repo_info)

    # Export to JSON
    output_file = "github_export.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=4)
        
    print(f"\nProcess completed! Data exported to {output_file}")

if __name__ == "__main__":
    main()