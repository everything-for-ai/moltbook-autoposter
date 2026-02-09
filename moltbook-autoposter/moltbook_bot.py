#!/usr/bin/env python3
"""
Moltbook Autoposter - 自动运营 Moltbook
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path


class MoltbookAutoposter:
    """Moltbook 自动运营机器人"""

    def __init__(self, config_file: str = "config.json"):
        self.config = self.load_config(config_file)
        self.credentials = self.load_credentials()
        self.base_url = "https://www.moltbook.com/api/v1"
        self.headers = {
            "Authorization": f"Bearer {self.credentials.get('api_key', '')}",
            "Content-Type": "application/json"
        }
        # 时间追踪
        self.last_like_time = datetime.now()
        self.last_follow_time = datetime.now()
        self.last_post_time = datetime.now()

    def load_config(self, config_file: str) -> Dict:
        """加载配置"""
        default_config = {
            "auto_post": {"enabled": False, "schedule": "09:00,14:00,20:00"},
            "auto_like": {"enabled": False, "interval_seconds": 60},
            "auto_reply": {"enabled": False, "keywords": []},
            "auto_follow": {"enabled": False, "interval_seconds": 120}
        }

        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                default_config.update(config)

        return default_config

    def load_credentials(self) -> Dict:
        """加载凭证"""
        cred_path = Path.home() / ".config" / "moltbook" / "credentials.json"
        default_creds = {
            "api_key": "",
            "agent_name": "CyberClaw2026"
        }

        if cred_path.exists():
            with open(cred_path, 'r', encoding='utf-8') as f:
                creds = json.load(f)
                default_creds.update(creds)

        return default_creds

    def get_feed(self, limit: int = 20) -> List[Dict]:
        """获取动态流"""
        try:
            url = f"{self.base_url}/posts"
            params = {"limit": limit}
            response = requests.get(url, headers=self.headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get("posts", []) if data.get("success") else []
        except Exception as e:
            print(f"获取动态失败: {e}")
        return []

    def like_post(self, post_id: str) -> bool:
        """点赞/顶帖"""
        try:
            url = f"{self.base_url}/posts/{post_id}/upvote"
            response = requests.post(url, headers=self.headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"点赞失败: {e}")
        return False

    def create_post(self, content: str, parent_id: Optional[str] = None) -> Optional[Dict]:
        """发布内容"""
        try:
            url = f"{self.base_url}/posts"
            data = {"content": content}
            if parent_id:
                data["parent_id"] = parent_id

            response = requests.post(url, headers=self.headers, json=data, timeout=10)

            if response.status_code in [200, 201]:
                return response.json()
        except Exception as e:
            print(f"发布失败: {e}")
        return None

    def get_comments(self, post_id: str) -> List[Dict]:
        """获取评论"""
        try:
            url = f"{self.base_url}/posts/{post_id}/comments"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return data.get("comments", []) if data.get("success") else []
        except Exception as e:
            print(f"获取评论失败: {e}")
        return []

    def reply_comment(self, parent_id: str, content: str) -> Optional[Dict]:
        """回复评论"""
        return self.create_post(content, parent_id=parent_id)

    def get_user_info(self, username: str) -> Optional[Dict]:
        """获取用户信息"""
        try:
            url = f"{self.base_url}/users/{username}"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"获取用户信息失败: {e}")
        return None

    def follow_user(self, username: str) -> bool:
        """关注用户"""
        try:
            url = f"{self.base_url}/users/{username}/follow"
            response = requests.post(url, headers=self.headers, timeout=10)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"关注失败: {e}")
        return False

    def auto_like(self):
        """自动点赞"""
        if not self.config.get("auto_like", {}).get("enabled", False):
            return

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 自动点赞...")
        feed = self.get_feed(10)

        for post in feed[:5]:
            post_id = post.get("id")
            if post_id and not post.get("liked", False):
                self.like_post(post_id)
                print(f"  点赞: {post.get('content', '')[:30]}...")
                time.sleep(2)  # 避免请求过快

    def auto_reply(self):
        """自动回复"""
        if not self.config.get("auto_reply", {}).get("enabled", False):
            return

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 自动回复...")
        keywords = self.config.get("auto_reply", {}).get("keywords", [])
        feed = self.get_feed(10)

        for post in feed:
            content = post.get("content", "").lower()
            if any(kw.lower() in content for kw in keywords):
                post_id = post.get("id")
                if post_id:
                    comments = self.get_comments(post_id)
                    # 只回复没有评论的帖子
                    if not comments:
                        reply_content = f"感谢分享！🙏 对这个话题感兴趣的朋友可以一起讨论"
                        self.reply_comment(post_id, reply_content)
                        print(f"  回复: {content[:30]}...")
                        break  # 每次只回复一条

    def auto_follow_feed(self):
        """自动关注动态流中的用户"""
        if not self.config.get("auto_follow", {}).get("enabled", False):
            return

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 自动关注...")
        feed = self.get_feed(20)

        for post in feed[:3]:
            author = post.get("author", {})
            username = author.get("username") if isinstance(author, dict) else None
            if username:
                self.follow_user(username)
                print(f"  关注: @{username}")
                time.sleep(2)

    def generate_content(self) -> str:
        """生成发布内容"""
        now = datetime.now().strftime("%H:%M")
        return f"🤖 自动测试 - {now}\n\nMoltbook Autoposter 运行正常！\n#AI #自动化"

    def auto_post(self):
        """自动发布"""
        if not self.config.get("auto_post", {}).get("enabled", False):
            return

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 自动发布...")
        content = self.generate_content()
        result = self.create_post(content)

        if result:
            print(f"  发布成功！")
        else:
            print(f"  发布失败")

    def run(self, run_once: bool = False):
        """主程序"""
        print("🚀 Moltbook Autoposter 启动！")
        print(f"Agent: {self.credentials.get('agent_name', 'Unknown')}")
        print("-" * 40)

        # 获取间隔配置
        like_interval = self.config.get("auto_like", {}).get("interval_seconds", 60)
        follow_interval = self.config.get("auto_follow", {}).get("interval_seconds", 120)
        post_interval = self.config.get("auto_post", {}).get("interval_seconds", 3600)

        if run_once:
            # 单次运行模式
            if self.config.get("auto_like", {}).get("enabled", False):
                self.auto_like()
            if self.config.get("auto_follow", {}).get("enabled", False):
                self.auto_follow_feed()
            if self.config.get("auto_post", {}).get("enabled", False):
                self.auto_post()
            return

        # 持续运行模式
        print("开始循环运行... (按 Ctrl+C 停止)")
        try:
            while True:
                now = datetime.now()

                # 自动点赞
                if self.config.get("auto_like", {}).get("enabled", False):
                    if now - self.last_like_time >= timedelta(seconds=like_interval):
                        self.auto_like()
                        self.last_like_time = now

                # 自动关注
                if self.config.get("auto_follow", {}).get("enabled", False):
                    if now - self.last_follow_time >= timedelta(seconds=follow_interval):
                        self.auto_follow_feed()
                        self.last_follow_time = now

                # 自动发布
                if self.config.get("auto_post", {}).get("enabled", False):
                    if now - self.last_post_time >= timedelta(seconds=post_interval):
                        self.auto_post()
                        self.last_post_time = now

                time.sleep(5)  # 每 5 秒检查一次

        except KeyboardInterrupt:
            print("\n👋 Moltbook Autoposter 已停止")


if __name__ == "__main__":
    bot = MoltbookAutoposter()
    bot.run()
