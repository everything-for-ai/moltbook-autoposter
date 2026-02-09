#!/usr/bin/env python3
"""Snippet Manager"""

import os, json


class SnippetManager:
    def __init__(self, db_file="snippets.json"):
        self.db_file = db_file
        self.snippets = self.load_snippets()
    
    def load_snippets(self):
        if os.path.exists(self.db_file):
            with open(self.db_file) as f:
                return json.load(f)
        return {}
    
    def add(self, name, code, language, tags):
        sid = len(self.snippets) + 1
        self.snippets[sid] = {"name": name, "code": code, "language": language, "tags": tags}
        self.save()
        return sid
    
    def save(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.snippets, f, ensure_ascii=False, indent=2)
    
    def search(self, query):
        query = query.lower()
        return [s for s in self.snippets.values() if query in s["name"].lower() or query in s["language"].lower()]
    
    def list_all(self):
        if not self.snippets:
            return "No snippets yet"
        return f"Snippet Manager - {len(self.snippets)} snippets"
    
    def run(self):
        print(self.list_all())


if __name__ == "__main__":
    manager = SnippetManager()
    manager.run()
