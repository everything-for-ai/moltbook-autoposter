#!/usr/bin/env python3
"""Meeting Notes"""

import os, json
from datetime import datetime


class MeetingNotes:
    def __init__(self, notes_file="meetings.json"):
        self.notes_file = notes_file
        self.meetings = self.load_meetings()
    
    def load_meetings(self):
        if os.path.exists(self.notes_file):
            with open(self.notes_file) as f:
                return json.load(f)
        return {}
    
    def add_meeting(self, title, date, attendees, notes, decisions, todos):
        mid = len(self.meetings) + 1
        self.meetings[mid] = {"title": title, "date": date, "attendees": attendees, "notes": notes, "decisions": decisions, "todos": todos, "created_at": datetime.now().isoformat()}
        self.save_meetings()
        return mid
    
    def save_meetings(self):
        with open(self.notes_file, 'w') as f:
            json.dump(self.meetings, f, ensure_ascii=False, indent=2)
    
    def get_latest_summary(self):
        if not self.meetings:
            return "No meetings yet"
        latest = list(self.meetings.values())[-1]
        return f"Latest: {latest['title']} ({latest['date']})"
    
    def run(self):
        print(self.get_latest_summary())


if __name__ == "__main__":
    notes = MeetingNotes()
    notes.run()
