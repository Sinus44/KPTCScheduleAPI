from pydantic import BaseModel

from src.schemes.bells_block_response import BellsBlockResponse


class ListBellBlocksResponse(BaseModel):
    bells: list[BellsBlockResponse]
