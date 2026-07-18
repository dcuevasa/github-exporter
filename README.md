# GitHub Data Exporter

This script exports information about all repositories where you are a collaborator or owner to a `.json` file. It includes repository metadata.

## Setup

1. Clone this repository.
2. Create a virtual environment and install the dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Generate a Personal Access Token (PAT) on GitHub with `repo` permissions.
4. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
5. Paste your token into the `.env` file.

## Usage

Run the script:

```bash
python export_github.py
```

The output will be saved to `github_export.json`.


