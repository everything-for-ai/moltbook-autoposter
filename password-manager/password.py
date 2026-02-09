#!/usr/bin/env python3
"""Password Manager"""

import os, json, random, string


class PasswordManager:
    def __init__(self, db_file="passwords.json"):
        self.db_file = db_file
        self.passwords = self.load_passwords()
    
    def load_passwords(self):
        if os.path.exists(self.db_file):
            with open(self.db_file) as f:
                return json.load(f)
        return {}
    
    def generate(self, length=16):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return "".join(random.choice(chars) for _ in range(length))
    
    def save(self, service, account, password):
        self.passwords[service] = {"account": account, "password": password, "created_at": "now"}
        with open(self.db_file, 'w') as f:
            json.dump(self.passwords, f, ensure_ascii=False, indent=2)
    
    def get(self, service):
        if service in self.passwords:
            p = self.passwords[service]
            return f"{service}: {p['account']} -> {p['password']}"
        return f"Not found: {service}"
    
    def list_services(self):
        if not self.passwords:
            return "No passwords saved"
        return "Services: " + ", ".join(self.passwords.keys())
    
    def run(self):
        print(self.list_services())


if __name__ == "__main__":
    manager = PasswordManager()
    manager.run()
