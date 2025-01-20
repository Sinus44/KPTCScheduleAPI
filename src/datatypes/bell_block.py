from src.datatypes.bell import Bell
from src.schemes.bells_block_response import BellsBlockResponse


class BellsBlock:
    def __init__(self):
        self.days: list[int] = []
        self.bells: list[Bell] = []

    def to_scheme(self):
        return BellsBlockResponse(days=self.days, bells=[bell.to_scheme() for bell in self.bells])
