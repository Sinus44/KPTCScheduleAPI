from pydantic import BaseModel


class LessonResponse(BaseModel):
    index: int
    discipline: str
    classroom: str
    classroom_raw: str
    time: str
    postfix: str
