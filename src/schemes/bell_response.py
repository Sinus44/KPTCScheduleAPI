from pydantic import BaseModel


class BellResponse(BaseModel):
    time_start: str
    time_end: str
    interval_type: int
