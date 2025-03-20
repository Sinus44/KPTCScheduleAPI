from json import loads

from src.datatypes.bell import Bell
from src.datatypes.bell_block import BellsBlock
from src.datatypes.list_bell_block import ListBellBlocks
from src.enums.intervaltype import IntervalType

with open("./bells_schedule.json") as file:
    BELLS = loads(file.read())


class BellService:
    def __init__(self):
        self.bells: dict[str, list[Bell]] = {}

        for key in BELLS:
            self.bells[key] = [Bell(bell["time_start"], bell["time_end"], bell["type"]) for bell in BELLS[key]]

    def get_all_bells(self) -> ListBellBlocks:
        bell_blocks: ListBellBlocks = ListBellBlocks()

        for key in self.bells:
            bell_block = BellsBlock()
            bell_block.days = list(map(int, key))
            bell_block.bells = self.bells[key]
            bell_blocks.blocks.append(bell_block)

        return bell_blocks

    def get_day_bells(self, day) -> list[Bell]:
        for key in self.bells:
            if str(day) in key:
                return self.bells[key]

        return []

    def get_all_lesson_bells(self):
        all_bells = self.get_all_bells()
        lesson_bells = ListBellBlocks()

        for block in all_bells.blocks:
            day = block.days[0]
            bells = self.get_day_lesson_bells(day)

            bell_block = BellsBlock()
            bell_block.days = block.days
            bell_block.bells = bells
            lesson_bells.blocks.append(bell_block)

        return lesson_bells

    def get_day_lesson_bells(self, day):
        bells: list[Bell] = self.get_day_bells(day)

        result = []

        i = 1
        while i < len(bells):
            c = bells[i]
            p = bells[i - 1]

            if c.interval_type == IntervalType.LESSON_CHANGE:
                n = bells[i + 1]
                result.append(Bell(p.time_start, n.time_end, IntervalType.LESSON))

                i += 3

            elif c.interval_type == IntervalType.LESSON and i == len(bells) - 1:
                result.append(c)
                i += 1

            else:
                if p.interval_type == IntervalType.LESSON:
                    result.append(p)

                i += 1

        return result
