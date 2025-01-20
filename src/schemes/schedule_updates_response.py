from pydantic import BaseModel

from src.schemes.schedule_update_response import ScheduleUpdateResponse


class ScheduleUpdatesResponse(BaseModel):
    updates: list[ScheduleUpdateResponse]
