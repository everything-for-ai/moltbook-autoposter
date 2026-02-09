#!/usr/bin/env python3
"""Book Notes Management"""

import os, json
from datetime import datetime


class BookNotes:
    def __init__(self, notes_file="books.json"):
        self.notes_file = notes_file
        self.books = self.load_books()
    
    def load_books(self):
        if os.path.exists(self.notes_file):
            with open(self.notes_file) as f:
                return json.load(f)
        return {}
    
    def add_book(self, title, author, notes, rating=0):
        book_id = len(self.books) + 1
        self.books[book_id] = {"title": title, "author": author, "notes": notes, "rating": rating, "added_at": datetime.now().isoformat()}
        self.save_books()
        return book_id
    
    def save_books(self):
        with open(self.notes_file, 'w') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=2)
    
    def list_books(self):
        if not self.books:
            return "No books yet"
        lines = ["Book List:"]
        for bid, book in self.books.items():
            lines.append(f"{bid}. {book['title']} - {book['author']}")
        return "\n".join(lines)


if __name__ == "__main__":
    notes = BookNotes()
    print(notes.list_books())
