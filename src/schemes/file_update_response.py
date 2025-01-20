from pydantic import BaseModel


class FileUpdateResponse(BaseModel):
    id: int
    update_file_id: str
    update_time: int
    update_type: int
