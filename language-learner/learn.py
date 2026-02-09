#!/usr/bin/env python3
"""
Language Learner - Daily vocabulary reminders
"""

import random
from datetime import datetime


class LanguageLearner:
    def __init__(self, vocab_file: str = "vocabulary.json"):
        self.vocab_file = vocab_file
        self.vocabulary = self.load_vocab()
    
    def load_vocab(self) -> list:
        return [
            {"word": "serendipity", "meaning": "意外发现珍宝", "sentence": "Finding this book was serendipity."},
            {"word": "ephemeral", "meaning": "短暂的", "sentence": "Fame in the digital age is often ephemeral."},
            {"word": "eloquent", "meaning": "雄辩的", "sentence": "She gave an eloquent speech."},
            {"word": "pragmatic", "meaning": "务实的", "sentence": "We need a pragmatic approach to this problem."},
            {"word": "ubiquitous", "meaning": "无处不在", "sentence": "Smartphones have become ubiquitous."}
        ]
    
    def get_daily_vocabulary(self, count: int = 3) -> str:
        words = random.sample(self.vocabulary, min(count, len(self.vocabulary)))
        
        lines = [f"📚 每日词汇 - {datetime.now().strftime('%Y-%m-%d')}\n"]
        
        for i, w in enumerate(words, 1):
            lines.append(f"{i}. {w['word']} ({w['meaning']})")
            lines.append(f"   📝 {w['sentence']}\n")
        
        return "\n".join(lines).strip()
    
    def add_word(self, word: str, meaning: str, sentence: str):
        self.vocabulary.append({
            "word": word,
            "meaning": meaning,
            "sentence": sentence
        })
        return len(self.vocabulary)
    
    def run(self):
        print(self.get_daily_vocabulary())
        return self.get_daily_vocabulary()


if __name__ == "__main__":
    learner = LanguageLearner()
    learner.run()
