from pydantic import BaseModel
from src.schemes.date_response import DateResponse


class ActualDatesResponse(BaseModel):
    actual_dates: list[DateResponse]
