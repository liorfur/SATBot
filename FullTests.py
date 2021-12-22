from HebrewChapter import HebrewChapter
from MathChapter import MathChapter
from EnglishChapter import EnglishChapter

class FullTest():
    # defines a full test with all three types of chapters included 
    def __init__(self):
        self.hebrew_chapter = HebrewChapter()
        self.math_chapter = MathChapter()
        self.english_chapter = EnglishChapter()
            
    def run_all(self):
        #runs and saves the most frequent answers to each type of chapter
        self.hebrew_chapter.get_questions()
        self.math_chapter.get_questions()
        self.english_chapter.get_questions()
