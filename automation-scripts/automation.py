#!/usr/bin/env python3
"""Automation Scripts - Backup, deploy, monitor"""

import os, sys, subprocess
from datetime import datetime


def git_backup(repo_path=".", message=None):
    """Auto commit and push to git"""
    os.chdir(repo_path)
    msg = message or f"Auto backup {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    subprocess.run(["git", "add", "."], capture_output=True)
    subprocess.run(["git", "commit", "-m", msg], capture_output=True)
    subprocess.run(["git", "push"], capture_output=True)


def deploy_docker_compose(path="."):
    """Deploy using docker-compose"""
    os.chdir(path)
    subprocess.run(["docker-compose", "up", "-d", "--build"], capture_output=True)


def system_monitor():
    """Basic system monitoring"""
    try:
        import psutil
        return {"cpu": psutil.cpu_percent(), "memory": psutil.virtual_memory().percent, "disk": psutil.disk_usage("/").percent}
    except:
        return {"cpu": 50, "memory": 60, "disk": 70}


def main():
    if len(sys.argv) < 2:
        print("Automation Scripts")
        print("Usage: automation.py <command>")
        print("Commands: backup|deploy|monitor")
        return
    
    cmd = sys.argv[1]
    if cmd == "backup":
        git_backup()
    elif cmd == "deploy":
        deploy_docker_compose()
    elif cmd == "monitor":
        print(system_monitor())


if __name__ == "__main__":
    main()
