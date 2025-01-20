from pydantic import BaseModel


class ScheduleUpdateResponse(BaseModel):
    id: int
    update_file_id: str
    update_time: int
    update_group: str
