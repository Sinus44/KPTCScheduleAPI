from src.datatypes.bell import Bell
from src.datatypes.bell_block import BellsBlock
from src.datatypes.list_bell_block import ListBellBlocks
from src.enums.intervaltype import IntervalType

BELLS = {
    "0": [
        {"time_start": "08:15", "time_end": "09:40", "type": IntervalType.LESSON},
        {"time_start": "09:40", "time_end": "10:00", "type": IntervalType.MIDDLE_CHANGE},
        {"time_start": "10:00", "time_end": "11:30", "type": IntervalType.LESSON},
        {"time_start": "11:30", "time_end": "12:00", "type": IntervalType.BIG_CHANGE},
        {"time_start": "12:00", "time_end": "12:30", "type": IntervalType.CONVERSATIONS},
        {"time_start": "12:40", "time_end": "13:25", "type": IntervalType.LESSON},
        {"time_start": "13:25", "time_end": "13:30", "type": IntervalType.LESSON_CHANGE},
        {"time_start": "13:30", "time_end": "14:15", "type": IntervalType.LESSON},
        {"time_start": "14:15", "time_end": "14:25", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "14:25", "time_end": "15:55", "type": IntervalType.LESSON},
        {"time_start": "15:55", "time_end": "16:05", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "16:05", "time_end": "17:35", "type": IntervalType.LESSON},
        {"time_start": "17:35", "time_end": "17:45", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "17:45", "time_end": "19:15", "type": IntervalType.LESSON},
        {"time_start": "19:15", "time_end": "19:25", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "19:25", "time_end": "20:55", "type": IntervalType.LESSON}
    ],
    "1234": [
        {"time_start": "08:15", "time_end": "09:40", "type": IntervalType.LESSON},
        {"time_start": "09:40", "time_end": "10:00", "type": IntervalType.MIDDLE_CHANGE},
        {"time_start": "10:00", "time_end": "10:45", "type": IntervalType.LESSON},
        {"time_start": "10:45", "time_end": "10:50", "type": IntervalType.LESSON_CHANGE},
        {"time_start": "10:50", "time_end": "11:35", "type": IntervalType.LESSON},
        {"time_start": "11:35", "time_end": "12:15", "type": IntervalType.BIG_CHANGE},
        {"time_start": "12:15", "time_end": "13:00", "type": IntervalType.LESSON},
        {"time_start": "13:00", "time_end": "13:05", "type": IntervalType.LESSON_CHANGE},
        {"time_start": "13:05", "time_end": "13:50", "type": IntervalType.LESSON},
        {"time_start": "13:50", "time_end": "14:00", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "14:00", "time_end": "14:45", "type": IntervalType.LESSON},
        {"time_start": "14:45", "time_end": "14:50", "type": IntervalType.LESSON_CHANGE},
        {"time_start": "14:50", "time_end": "15:35", "type": IntervalType.LESSON},
        {"time_start": "15:35", "time_end": "15:45", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "15:45", "time_end": "16:30", "type": IntervalType.LESSON},
        {"time_start": "16:30", "time_end": "16:35", "type": IntervalType.LESSON_CHANGE},
        {"time_start": "16:35", "time_end": "17:20", "type": IntervalType.LESSON},
        {"time_start": "17:20", "time_end": "17:30", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "17:30", "time_end": "18:50", "type": IntervalType.LESSON},
        {"time_start": "18:50", "time_end": "19:00", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "19:00", "time_end": "20:20", "type": IntervalType.LESSON}
    ],
    "5": [
        {"time_start": "08:15", "time_end": "09:00", "type": IntervalType.LESSON},
        {"time_start": "09:00", "time_end": "09:05", "type": IntervalType.LESSON_CHANGE},
        {"time_start": "09:05", "time_end": "09:50", "type": IntervalType.LESSON},
        {"time_start": "09:50", "time_end": "10:00", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "10:00", "time_end": "10:45", "type": IntervalType.LESSON},
        {"time_start": "10:45", "time_end": "10:50", "type": IntervalType.LESSON_CHANGE},
        {"time_start": "10:50", "time_end": "11:35", "type": IntervalType.LESSON},
        {"time_start": "11:35", "time_end": "11:45", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "11:45", "time_end": "12:30", "type": IntervalType.LESSON},
        {"time_start": "12:30", "time_end": "12:35", "type": IntervalType.LESSON_CHANGE},
        {"time_start": "12:35", "time_end": "13:20", "type": IntervalType.LESSON},
        {"time_start": "13:20", "time_end": "13:30", "type": IntervalType.LITTLE_CHANGE},
        {"time_start": "13:30", "time_end": "14:15", "type": IntervalType.LESSON},
        {"time_start": "14:15", "time_end": "14:20", "type": IntervalType.LESSON_CHANGE},
        {"time_start": "14:20", "time_end": "15:05", "type": IntervalType.LESSON}
    ]
}


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
