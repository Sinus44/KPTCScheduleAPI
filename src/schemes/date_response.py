from pydantic import BaseModel


class DateResponse(BaseModel):
    full: str
    day: int
    month: int
    year: int
    weekday_index: int
    weekday_name: str
