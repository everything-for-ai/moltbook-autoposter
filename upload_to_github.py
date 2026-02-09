#!/usr/bin/env python3
"""
GitHub Uploader - Upload projects to everything-for-ai organization
"""

import os
import json
import base64
import requests
from datetime import datetime


GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
ORG = "everything-for-ai"


class GitHubUploader:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.base_url = "https://api.github.com"
    
    def create_or_update_file(self, repo: str, path: str, content: str, message: str):
        """Create or update a file in the repository"""
        url = f"{self.base_url}/repos/{ORG}/{repo}/contents/{path}"
        
        # Get current file SHA if it exists
        response = requests.get(url, headers=self.headers)
        sha = None
        if response.status_code == 200:
            sha = response.json().get("sha")
        
        # Prepare data
        data = {
            "message": message,
            "content": base64.b64encode(content.encode()).decode(),
        }
        if sha:
            data["sha"] = sha
        
        # Create or update
        response = requests.put(url, headers=self.headers, json=data)
        
        if response.status_code in [200, 201]:
            print(f"✓ {repo}/{path}")
            return True
        else:
            print(f"✗ {repo}/{path}: {response.json().get('message')}")
            return False
    
    def upload_project(self, project_dir: str, repo_name: str):
        """Upload all files from a project directory"""
        print(f"\n📤 上传 {repo_name}...")
        
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith(('.pyc', '__pycache__', '.git')):
                    continue
                
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, project_dir)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                message = f"Add {rel_path}"
                self.create_or_update_file(repo_name, rel_path, content, message)
    
    def create_readme(self, repo: str, description: str):
        """Create README.md for repository"""
        readme_content = f"""# {repo}

{description}

## Getting Started

```bash
git clone https://github.com/{ORG}/{repo}.git
cd {repo}
pip install -r requirements.txt
```

## Usage

```bash
python *.py
```

## License

MIT
"""
        self.create_or_update_file(repo, "README.md", readme_content, "Add README")


def main():
    uploader = GitHubUploader(GITHUB_TOKEN)
    
    projects = [
        ("weather-bot", "Multi-platform weather notification bot"),
        ("daily-report-generator", "AI-powered daily report generator"),
        ("joke-bot", "Daily jokes and fun facts delivery bot"),
        ("inspiration-bot", "Daily quotes and inspiration delivery"),
        ("weekly-summary", "Weekly progress summary and review bot"),
        ("todo-bot", "AI-powered todo list and task management bot"),
    ]
    
    for project_dir, description in projects:
        if os.path.exists(f"/root/.openclaw/workspace/everything-for-ai/{project_dir}"):
            uploader.create_readme(project_dir, description)
            uploader.upload_project(f"/root/.openclaw/workspace/everything-for-ai/{project_dir}", project_dir)
    
    print("\n✅ 上传完成!")


if __name__ == "__main__":
    main()
