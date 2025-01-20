from pydantic import BaseModel

from src.schemes.file_response import FileResponse


class FilesResponse(BaseModel):
    files: list[FileResponse]
