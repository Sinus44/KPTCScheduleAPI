from pydantic import BaseModel


class GroupNamesResponse(BaseModel):
    group_names: list[str]
