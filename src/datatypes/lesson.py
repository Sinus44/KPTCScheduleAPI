import copy

from src.schemes.lesson_response import LessonResponse


class Lesson:
    def __init__(self):
        self.index = -1
        self.discipline = ""
        self.classroom_raw = ""
        self.time = ""
        self.postfix = ""
        self.classroom = ""

    def serialize(self):
        return LessonResponse(index=self.index, discipline=self.discipline, classroom_raw=self.classroom_raw,
                              classroom=self.classroom, time=self.time, postfix=self.postfix)

    def to_dict(self):
        return copy.deepcopy(self.__dict__)
