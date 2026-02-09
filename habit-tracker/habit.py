#!/usr/bin/env python3
"""Habit Tracker"""

import os, json
from datetime import datetime, timedelta


class HabitTracker:
    def __init__(self, db_file="habits.json"):
        self.db_file = db_file
        self.habits = self.load_habits()
    
    def load_habits(self):
        if os.path.exists(self.db_file):
            with open(self.db_file) as f:
                return json.load(f)
        return {}
    
    def add_habit(self, name, goal="daily"):
        hid = len(self.habits) + 1
        self.habits[hid] = {"name": name, "goal": goal, "streak": 0, "last_completed": None, "created_at": datetime.now().isoformat()}
        self.save_habits()
        return hid
    
    def complete(self, habit_id):
        if habit_id not in self.habits:
            return False
        habit = self.habits[habit_id]
        today = datetime.now().strftime("%Y-%m-%d")
        if habit.get("last_completed") != today:
            habit["last_completed"] = today
            habit["streak"] = habit.get("streak", 0) + 1
            self.save_habits()
        return True
    
    def save_habits(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.habits, f, ensure_ascii=False, indent=2)
    
    def get_status(self):
        if not self.habits:
            return "No habits yet"
        lines = [f"Habit Tracker - {len(self.habits)} habits"]
        for hid, h in self.habits.items():
            lines.append(f"- {h['name']}: {h.get('streak', 0)} day streak")
        return "\n".join(lines)
    
    def run(self):
        print(self.get_status())


if __name__ == "__main__":
    tracker = HabitTracker()
    tracker.run()
