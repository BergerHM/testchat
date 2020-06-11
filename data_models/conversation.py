#Test
from enum import Enum


class Question(Enum):
    EXPERT = 1
    ACCEPT = 2
    HAPPY = 3
    NONE = 4


class Conversation:
    def __init__(
            self, last_question_asked: Question = Question.NONE,
    ):
        self.last_question_asked = last_question_asked
