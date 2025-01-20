from pydantic import BaseModel


class FolderLinkResponse(BaseModel):
    folder_link: str
