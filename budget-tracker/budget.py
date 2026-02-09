#!/usr/bin/env python3
"""Budget Tracker - Personal finance management"""

import os, json
from datetime import datetime


class BudgetTracker:
    def __init__(self, db_file="budget.json"):
        self.db_file = db_file
        self.data = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.db_file):
            with open(self.db_file) as f:
                return json.load(f)
        return {"budget": 0, "expenses": []}
    
    def set_budget(self, amount):
        self.data["budget"] = amount
        self.save_data()
    
    def add_expense(self, category, amount, description=""):
        self.data["expenses"].append({"category": category, "amount": amount, "description": description, "date": datetime.now().strftime("%Y-%m-%d")})
        self.save_data()
    
    def save_data(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_summary(self):
        budget = self.data.get("budget", 0)
        expenses = self.data.get("expenses", [])
        total = sum(e["amount"] for e in expenses)
        remaining = budget - total
        return f"Budget: {budget}, Spent: {total}, Remaining: {remaining}"
    
    def run(self):
        print(self.get_summary())


if __name__ == "__main__":
    tracker = BudgetTracker()
    tracker.run()
