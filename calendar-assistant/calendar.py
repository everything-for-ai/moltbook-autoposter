#!/usr/bin/env python3
"""Calendar Assistant - Smart scheduling"""

import os, json
from datetime import datetime, timedelta


class CalendarAssistant:
    def __init__(self, events_file="events.json"):
        self.events_file = events_file
        self.events = self.load_events()
    
    def load_events(self):
        if os.path.exists(self.events_file):
            with open(self.events_file) as f:
                return json.load(f)
        return {}
    
    def add_event(self, title, date, time=None, duration=60, description=""):
        event_id = len(self.events) + 1
        self.events[event_id] = {"title": title, "date": date, "time": time, "duration": duration, "description": description}
        self.save_events()
        return event_id
    
    def save_events(self):
        with open(self.events_file, 'w') as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2)
    
    def get_today_events(self):
        today = datetime.now().strftime("%Y-%m-%d")
        todays = [e for e in self.events.values() if e["date"] == today]
        return f"Today ({today}): {len(todays)} events"
    
    def run(self):
        print(self.get_today_events())


if __name__ == "__main__":
    assistant = CalendarAssistant()
    assistant.run()
