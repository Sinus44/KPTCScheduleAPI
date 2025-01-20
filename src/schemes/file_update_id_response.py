from pydantic import BaseModel


class UpdateIdResponse(BaseModel):
    id: int
