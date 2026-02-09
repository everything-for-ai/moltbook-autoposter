#!/usr/bin/env python3
"""GitHub Notification Bot"""

import os, json, requests
from datetime import datetime


class GitHubNotificationBot:
    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)
        self.headers = {"Authorization": f"token {self.config.get('github_token', os.environ.get('GITHUB_TOKEN', ''))}", "Accept": "application/vnd.github.v3+json"}
    
    def load_config(self, config_file):
        default_config = {"username": "", "watch_repos": []}
        if os.path.exists(config_file):
            with open(config_file) as f:
                default_config.update(json.load(f))
        return default_config
    
    def get_notifications(self):
        try:
            response = requests.get("https://api.github.com/notifications", headers=self.headers, params={"participating": "true", "per_page": 10}, timeout=10)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return []
    
    def format_notifications(self, notifications):
        if not notifications:
            return "No new GitHub notifications"
        lines = [f"GitHub Notifications - {datetime.now().strftime('%H:%M')}"]
        for n in notifications[:5]:
            repo = n["repository"]["full_name"]
            title = n.get("subject", {}).get("title", "No title")
            lines.append(f"- {repo}: {title}")
        return "\n".join(lines)
    
    def run(self):
        notifications = self.get_notifications()
        message = self.format_notifications(notifications)
        print(message)
        return message


if __name__ == "__main__":
    bot = GitHubNotificationBot()
    bot.run()
