from pydantic import BaseModel

from src.schemes.file_update_response import FileUpdateResponse


class FileUpdatesResponse(BaseModel):
    updates: list[FileUpdateResponse]
