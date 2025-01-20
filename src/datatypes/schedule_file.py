from src.enums.weekday_name import get_weekday_name_by_index
from src.schemes.date_response import DateResponse
from src.schemes.file_response import FileResponse
from src.services.check_actual_service import check_actual


class File:
    @property
    def is_actual(self):
        return check_actual(self.date)

    def __init__(self):
        self.last_update = 0
        self.name = ""
        self.date = ""
        self.id = ""
        self.weekday_index = 0

    def serialize_date(self):
        day, month, year = list(map(int, self.date.split(".")))
        return DateResponse(full=self.date, day=day, month=month, year=year, weekday_index=self.weekday_index,
                            weekday_name=get_weekday_name_by_index(self.weekday_index))

    def serialize(self):
        return FileResponse(last_update=self.last_update, name=self.name, date=self.serialize_date(), id=self.id, is_actual=self.is_actual)

    def date_to_scheme(self):
        day, month, year = list(map(int, self.date.split(".")))
        return DateResponse(full=self.date, day=day, month=month, year=year, weekday_index=self.weekday_index,
                            weekday_name=get_weekday_name_by_index(self.weekday_index))

    def to_scheme(self):
        return FileResponse(last_update=self.last_update, name=self.name, date=self.date_to_scheme(), id=self.id, is_actual=self.is_actual)

