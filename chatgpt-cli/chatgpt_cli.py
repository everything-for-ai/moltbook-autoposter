#!/usr/bin/env python3
"""ChatGPT CLI"""

import os, sys, json


def load_config():
    config_file = os.path.expanduser("~/.chatgpt-cli.json")
    if os.path.exists(config_file):
        with open(config_file) as f:
            return json.load(f)
    return {"api_key": os.environ.get("OPENAI_API_KEY", ""), "model": "gpt-4"}


def chat(prompt):
    config = load_config()
    if config["api_key"]:
        print(f"[AI] Would call OpenAI API with: {prompt[:50]}...")
    else:
        print(f"[Mock AI] {prompt[:30]}... (Configure OPENAI_API_KEY for real AI)")


def main():
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        chat(prompt)
    else:
        print("ChatGPT CLI - Configure OPENAI_API_KEY to use")
        print("Usage: chatgpt 'your question'")


if __name__ == "__main__":
    main()
