#Test
from enum import Enum


class Question(Enum):
    NAME = 1
    ROLLE = 2
    NONE = 3


class Conversation:
    def __init__(
            self, last_question_asked: Question = Question.NONE,
    ):
        self.last_question_asked = last_question_asked
