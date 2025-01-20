from pydantic import BaseModel

from src.schemes.file_response import FileResponse
from src.schemes.group_response import GroupResponse


class ScheduleGroupResponse(BaseModel):
    file: FileResponse
    group: GroupResponse
