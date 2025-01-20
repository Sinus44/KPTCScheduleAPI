from pydantic import BaseModel

from src.schemes.bell_response import BellResponse


class BellsBlockResponse(BaseModel):
    days: list[int]
    bells: list[BellResponse]
