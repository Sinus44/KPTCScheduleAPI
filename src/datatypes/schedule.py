from src.datatypes.group import Group
from src.datatypes.schedule_file import File
from src.schemes.schedule_response import ScheduleResponse


class Schedule:
    def __init__(self, file: File, groups: list[Group]):
        self.file: File = file
        self.groups: list[Group] = groups

    def serialize(self):
        return {"file": self.file.serialize(), "groups": [group.serialize() for group in self.groups]}

    def to_scheme(self):
        return ScheduleResponse(file=self.file.to_scheme(), groups=[group.to_scheme() for group in self.groups])
