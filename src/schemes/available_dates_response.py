from pydantic import BaseModel
from src.schemes.date_response import DateResponse


class AvailableDatesResponse(BaseModel):
    available_dates: list[DateResponse]
