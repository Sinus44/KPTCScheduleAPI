from pydantic import BaseModel

from src.schemes.date_response import DateResponse


class FileResponse(BaseModel):
    last_update: int
    name: str
    date: DateResponse
    id: str
    is_actual: bool
