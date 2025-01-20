from pydantic import BaseModel

from src.schemes.schedule_response import ScheduleResponse


class SchedulesResponse(BaseModel):
    schedule: list[ScheduleResponse]
