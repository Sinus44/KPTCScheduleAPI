from src.schemes.bell_response import BellResponse


class Bell:
    def __init__(self, time_start="", time_end="", interval_type=-1):
        self.time_start: str = time_start
        self.time_end: str = time_end
        self.interval_type: int = interval_type

    def serialize(self):
        return BellResponse(time_start=self.time_start, time_end=self.time_end, interval_type=self.interval_type)

    def to_scheme(self):
        return BellResponse(time_start=self.time_start, time_end=self.time_end, interval_type=self.interval_type)
