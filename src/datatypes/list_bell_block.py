from src.datatypes.bell_block import BellsBlock
from src.schemes.list_bell_blocks_response import ListBellBlocksResponse


class ListBellBlocks:
    def __init__(self):
        self.blocks: list[BellsBlock] = []

    def to_scheme(self):
        return ListBellBlocksResponse(bells=[block.to_scheme() for block in self.blocks])
