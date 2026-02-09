#!/usr/bin/env python3
"""
GitHub Stats Tracker - Track and visualize GitHub activity
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List


class GitHubStatsTracker:
    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.headers = {
            "Authorization": f"token {self.config.get('github_token', os.environ.get('GITHUB_TOKEN', ''))}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def load_config(self, config_file: str) -> Dict:
        default_config = {
            "schedule": "09:00",
            "platforms": ["feishu"],
            "username": ""
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
                default_config.update(config)
        
        return default_config
    
    def get_user_stats(self, username: str) -> Dict:
        """Get user profile stats"""
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return {}
    
    def get_user_repos(self, username: str) -> List[Dict]:
        """Get user repositories"""
        url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json()
        return []
    
    def get_user_events(self, username: str) -> List[Dict]:
        """Get user public events"""
        url = f"https://api.github.com/users/{username}/events/public?per_page=10"
        response = requests.get(url, headers=self.headers)
        
        if response.json():
            return response.json()
        return []
    
    def format_stats_message(self, username: str) -> str:
        """Format stats as a message"""
        profile = self.get_user_stats(username)
        repos = self.get_user_repos(username)
        
        if not profile:
            return f"无法获取用户 {username} 的信息"
        
        public_repos = profile.get("public_repos", 0)
        followers = profile.get("followers", 0)
        following = profile.get("following", 0)
        created_at = profile.get("created_at", "")[:10]
        
        top_repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)[:5]
        
        repo_list = ""
        for i, repo in enumerate(top_repos, 1):
            stars = repo.get("stargazers_count", 0)
            repo_list += f"{i}. {repo['name']} ⭐{stars}\n"
        
        return f"""
📊 GitHub Stats - {username}

👥 粉丝: {followers} | 关注: {following}
📦 公开仓库: {public_repos} 个
📅 加入时间: {created_at}

🔥 Top 仓库:
{repo_list.strip() or '暂无数据'}
        """.strip()
    
    def run(self):
        username = self.config.get("username", "")
        if not username:
            print("未配置用户名")
            return
        
        message = self.format_stats_message(username)
        print(message)
        return message


if __name__ == "__main__":
    tracker = GitHubStatsTracker()
    tracker.run()
