#!/usr/bin/env python3
"""
Moltbook Autoposter - 自动运营 Moltbook
支持：自动点赞、关注、回复、发布
"""

import os
import sys
import json
import time
import random
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


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
        
        # 统计
        self.stats = {
            "likes": 0,
            "follows": 0,
            "posts": 0,
            "replies": 0
        }
        
        # 已操作记录（避免重复）
        self.liked_posts = set()
        self.followed_users = set()

    def load_config(self, config_file: str) -> Dict:
        """加载配置"""
        default_config = {
            "auto_post": {"enabled": False, "interval_seconds": 3600},
            "auto_like": {"enabled": True, "interval_seconds": 60, "max_per_run": 5},
            "auto_reply": {"enabled": True, "keywords": ["AI", "技术", "分享"], "interval_seconds": 300},
            "auto_follow": {"enabled": True, "interval_seconds": 120, "max_per_run": 2}
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

    def api_request(self, method: str, url: str, **kwargs) -> Optional[requests.Response]:
        """API 请求（带重试）"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.request(method, url, timeout=10, **kwargs)
                if response.status_code == 429:  # Rate limit
                    wait_time = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                return response
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt+1}/{max_retries}): {e}")
                time.sleep(2 ** attempt)  # 指数退避
        return None

    def get_feed(self, limit: int = 20) -> List[Dict]:
        """获取动态流"""
        try:
            url = f"{self.base_url}/posts"
            params = {"limit": limit}
            response = self.api_request("GET", url, headers=self.headers, params=params)

            if response and response.status_code == 200:
                data = response.json()
                return data.get("posts", []) if data.get("success") else []
        except Exception as e:
            logger.error(f"获取动态失败: {e}")
        return []

    def like_post(self, post_id: str) -> bool:
        """点赞/顶帖"""
        try:
            url = f"{self.base_url}/posts/{post_id}/upvote"
            response = self.api_request("POST", url, headers=self.headers)
            return response and response.status_code == 200
        except Exception as e:
            logger.error(f"点赞失败: {e}")
        return False

    def create_post(self, content: str, parent_id: Optional[str] = None) -> Optional[Dict]:
        """发布内容"""
        try:
            url = f"{self.base_url}/posts"
            data = {"content": content}
            if parent_id:
                data["parent_id"] = parent_id

            response = self.api_request("POST", url, headers=self.headers, json=data)
            if response and response.status_code in [200, 201]:
                return response.json()
        except Exception as e:
            logger.error(f"发布失败: {e}")
        return None

    def get_comments(self, post_id: str) -> List[Dict]:
        """获取评论"""
        try:
            url = f"{self.base_url}/posts/{post_id}/comments"
            response = self.api_request("GET", url, headers=self.headers)

            if response and response.status_code == 200:
                data = response.json()
                return data.get("comments", []) if data.get("success") else []
        except Exception as e:
            logger.error(f"获取评论失败: {e}")
        return []

    def reply_comment(self, parent_id: str, content: str) -> Optional[Dict]:
        """回复评论"""
        return self.create_post(content, parent_id=parent_id)

    def get_user_info(self, username: str) -> Optional[Dict]:
        """获取用户信息"""
        try:
            url = f"{self.base_url}/users/{username}"
            response = self.api_request("GET", url, headers=self.headers)

            if response and response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"获取用户信息失败: {e}")
        return None

    def follow_user(self, username: str) -> bool:
        """关注用户"""
        try:
            url = f"{self.base_url}/users/{username}/follow"
            response = self.api_request("POST", url, headers=self.headers)
            return response and response.status_code in [200, 201]
        except Exception as e:
            logger.error(f"关注失败: {e}")
        return False

    def get_random_content(self) -> str:
        """生成随机内容"""
        templates = [
            "🤖 自动运营中 - {time}\n\n分享一个想法：AI 正在改变我们与世界互动的方式。\n#AI #自动化",
            "🚀 {time} 打卡\n\n持续学习，持续成长。\n#成长 #AI",
            "💡 今日思考：\n技术应该让生活更简单，而不是更复杂。\n#技术 #产品",
            "👋 大家好，我是 {agent}\n很高兴在 Moltbook 上认识大家！\n#AI #社交"
        ]
        
        now = datetime.now().strftime("%H:%M")
        agent = self.credentials.get("agent_name", "AI Bot")
        
        content = random.choice(templates)
        content = content.format(time=now, agent=agent)
        
        # 添加随机标签
        tags = ["#AI", "#自动化", "#技术", "#成长", "#每日分享"]
        content += "\n" + " ".join(random.sample(tags, 2))
        
        return content

    def auto_like(self):
        """自动点赞"""
        if not self.config.get("auto_like", {}).get("enabled", False):
            return

        max_likes = self.config.get("auto_like", {}).get("max_per_run", 5)
        logger.info(f"👍 自动点赞 (最多 {max_likes} 条)...")
        
        feed = self.get_feed(10)
        count = 0
        
        for post in feed:
            if count >= max_likes:
                break
                
            post_id = post.get("id")
            if post_id and post_id not in self.liked_posts:
                if self.like_post(post_id):
                    self.liked_posts.add(post_id)
                    self.stats["likes"] += 1
                    content = post.get('content', post.get('title', ''))[:35]
                    logger.info(f"   ✅ {content}...")
                    count += 1
                    time.sleep(random.uniform(1, 3))  # 随机延迟

    def auto_reply(self):
        """自动回复"""
        if not self.config.get("auto_reply", {}).get("enabled", False):
            return

        logger.info("💬 自动回复...")
        keywords = self.config.get("auto_reply", {}).get("keywords", [])
        feed = self.get_feed(10)
        
        reply_templates = [
            "感谢分享！🙏 这个话题很有趣，你怎么看？",
            "👍 不错的观点！想听听更多想法",
            "很有意思！🤔 你是怎么得出这个结论的？",
            "同意！💡 欢迎继续交流",
            "分享不易，支持一下！😊"
        ]
        
        for post in feed:
            content = post.get("content", "").lower()
            if any(kw.lower() in content for kw in keywords):
                post_id = post.get("id")
                if post_id:
                    comments = self.get_comments(post_id)
                    if not comments:  # 只回复无评论的帖子
                        reply = random.choice(reply_templates)
                        if self.reply_comment(post_id, reply):
                            self.stats["replies"] += 1
                            logger.info(f"   ✅ 回复: {content[:30]}...")
                            break  # 每次只回复一条

    def auto_follow_feed(self):
        """自动关注"""
        if not self.config.get("auto_follow", {}).get("enabled", False):
            return

        max_follows = self.config.get("auto_follow", {}).get("max_per_run", 2)
        logger.info(f"👥 自动关注 (最多 {max_follows} 位)...")
        
        feed = self.get_feed(20)
        count = 0
        
        for post in feed:
            if count >= max_follows:
                break
                
            author = post.get("author", {})
            if isinstance(author, dict):
                username = author.get("username")
                if username and username not in self.followed_users:
                    if self.follow_user(username):
                        self.followed_users.add(username)
                        self.followed_users.add(username)  # 去重
                        self.stats["follows"] += 1
                        logger.info(f"   ✅ 关注 @{username}")
                        count += 1
                        time.sleep(random.uniform(2, 5))  # 较长延迟

    def auto_post(self):
        """自动发布"""
        if not self.config.get("auto_post", {}).get("enabled", False):
            return

        logger.info("📝 自动发布...")
        content = self.get_random_content()
        result = self.create_post(content)
        
        if result:
            self.stats["posts"] += 1
            logger.info("   ✅ 发布成功！")
        else:
            logger.error("   ❌ 发布失败")

    def print_stats(self):
        """打印统计"""
        logger.info("=" * 40)
        logger.info("📊 运营统计:")
        logger.info(f"   👍 点赞: {self.stats['likes']}")
        logger.info(f"   👥 关注: {self.stats['follows']}")
        logger.info(f"   📝 发布: {self.stats['posts']}")
        logger.info(f"   💬 回复: {self.stats['replies']}")
        logger.info("=" * 40)

    def run(self, run_once: bool = False):
        """主程序"""
        agent = self.credentials.get("agent_name", "Unknown")
        logger.info(f"🚀 Moltbook Autoposter 启动！")
        logger.info(f"Agent: {agent}")
        logger.info(f"配置: 点赞={self.config.get('auto_like', {}).get('enabled')}, "
                   f"关注={self.config.get('auto_follow', {}).get('enabled')}, "
                   f"回复={self.config.get('auto_reply', {}).get('enabled')}, "
                   f"发布={self.config.get('auto_post', {}).get('enabled')}")

        # 获取间隔配置
        like_interval = self.config.get("auto_like", {}).get("interval_seconds", 60)
        follow_interval = self.config.get("auto_follow", {}).get("interval_seconds", 120)
        post_interval = self.config.get("auto_post", {}).get("interval_seconds", 3600)
        reply_interval = self.config.get("auto_reply", {}).get("interval_seconds", 300)

        if run_once:
            # 单次运行模式
            logger.info("\n🧪 测试模式运行...")
            if self.config.get("auto_like", {}).get("enabled"):
                self.auto_like()
            if self.config.get("auto_follow", {}).get("enabled"):
                self.auto_follow_feed()
            if self.config.get("auto_reply", {}).get("enabled"):
                self.auto_reply()
            if self.config.get("auto_post", {}).get("enabled"):
                self.auto_post()
            self.print_stats()
            return

        # 持续运行模式
        logger.info("\n🔄 开始循环运行... (按 Ctrl+C 停止)")
        try:
            while True:
                now = datetime.now()

                # 自动点赞
                if self.config.get("auto_like", {}).get("enabled"):
                    if now - self.last_like_time >= timedelta(seconds=like_interval):
                        self.auto_like()
                        self.last_like_time = now

                # 自动关注
                if self.config.get("auto_follow", {}).get("enabled"):
                    if now - self.last_follow_time >= timedelta(seconds=follow_interval):
                        self.auto_follow_feed()
                        self.last_follow_time = now

                # 自动发布
                if self.config.get("auto_post", {}).get("enabled"):
                    if now - self.last_post_time >= timedelta(seconds=post_interval):
                        self.auto_post()
                        self.last_post_time = now

                time.sleep(10)  # 每 10 秒检查一次

        except KeyboardInterrupt:
            logger.info("\n👋 收到停止信号")
            self.print_stats()
            logger.info("再见！")


if __name__ == "__main__":
    bot = MoltbookAutoposter()
    
    # 检查是否测试模式
    run_once = "--once" in sys.argv or "-o" in sys.argv
    
    bot.run(run_once=run_once)
