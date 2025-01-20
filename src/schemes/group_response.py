from pydantic import BaseModel

from src.schemes.lesson_response import LessonResponse


class GroupResponse(BaseModel):
    name: str
    course: int
    sub_group: int
    spec: str
    school_year: int
    lessons: list[LessonResponse]
