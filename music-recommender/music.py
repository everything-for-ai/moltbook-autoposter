#!/usr/bin/env python3
"""
Music Recommender
"""

import random


class MusicRecommender:
    def __init__(self, config_file: str = "config.json"):
        self.songs = self.load_songs()
    
    def load_songs(self) -> list:
        return [
            {"title": "热门歌曲 A", "artist": "歌手 A", "genre": "pop"},
            {"title": "轻音乐 B", "artist": "歌手 B", "genre": "instrumental"},
            {"title": "摇滚 C", "artist": "歌手 C", "genre": "rock"},
            {"title": "爵士 D", "artist": "歌手 D", "genre": "jazz"},
            {"title": "电子 E", "artist": "歌手 E", "genre": "electronic"}
        ]
    
    def recommend(self, genre: str = None) -> dict:
        if genre:
            songs = [s for s in self.songs if s["genre"] == genre]
            if songs:
                return random.choice(songs)
        return random.choice(self.songs)
    
    def get_daily_recommendation(self) -> str:
        song = self.recommend()
        return f"""
🎵 每日音乐推荐

🎤 {song['title']}
👤 {song['artist']}
🏷️ {song['genre'].capitalize()}

#音乐推荐
        """.strip()
    
    def run(self):
        print(self.get_daily_recommendation())
        return self.get_daily_recommendation()


if __name__ == "__main__":
    recommender = MusicRecommender()
    recommender.run()
