import logging
from threading import Thread

from src.datatypes.group import Group
from src.datatypes.schedule import Schedule
from src.datatypes.schedule_file import File
from src.parse_html import parse_html
from src.services.bell_service import BellService
from src.services.file_service import FileService


def filter_group(schedule: Schedule, group_name: str) -> Group | None:
    for group in schedule.groups:
        if group.name.lower() == group_name.lower():
            return group

    logging.warning(f"Not found group {group_name} in {[group.name for group in schedule.groups]}")
    return None


def filter_group_in_schedule(schedule: Schedule, group_name: str) -> Schedule:
    groups = []
    new_group = filter_group(schedule, group_name)
    if new_group is not None:
        groups.append(new_group)

    return Schedule(schedule.file, groups)


def filter_group_by_schedule_list(schedules: list[Schedule], group_name: str) -> list[Schedule]:
    return [filter_group_in_schedule(schedule, group_name) for schedule in schedules]


def filter_group_by_schedule_list_old(schedules: list[Schedule], group_name: str) -> list[Schedule]:
    filtered_schedule_list = []

    for schedule in schedules:
        file = schedule.file
        filtered_group = filter_group(schedule, group_name)
        filtered_schedule = Schedule(file=file, groups=[filtered_group])
        filtered_schedule_list.append(filtered_schedule)

    return filtered_schedule_list


class ScheduleService:
    def __init__(self, file_controller, bells_controller):
        self.file_controller: FileService = file_controller
        self.bells_controller: BellService = bells_controller
        self.schedule: list[Schedule] = []

    def get_schedule_by_id_or_none(self, file_id):
        for schedule in self.schedule:
            if schedule.file.id == file_id:
                return schedule

    def update_or_get_schedule_by_id(self, file):
        schedule = self.get_schedule_by_id_or_none(file.id)

        if schedule is not None:
            return schedule

        else:
            loaded = self.load(file)
            return loaded

    def load(self, file):
        groups = parse_html(file.id)
        groups = self.connect_time(groups, file)
        schedule = Schedule(file, groups)
        self.schedule.append(schedule)
        return schedule

    def update_list(self, files: list[File]):
        file_ids = [file.id for file in files]

        pop_ids = []
        for i, schedule in enumerate(self.schedule):
            if schedule.file.id in file_ids:
                pop_ids.append(i)

        for pop_id in pop_ids[::-1]:
            self.schedule.pop(pop_id)

        threads = []
        for file in files:
            t = Thread(target=self.load, args=(file,))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        return self.schedule

    def connect_time(self, schedule, file):
        day_calls = self.bells_controller.get_day_lesson_bells(file.weekday_index)

        for group in schedule:
            for lesson in group.lessons:
                call_index = lesson.index - 1

                if 0 <= call_index < len(day_calls):
                    lesson_time = day_calls[call_index]
                    formated_time = f"{lesson_time.time_start} - {lesson_time.time_end}"

                else:
                    formated_time = f"--:-- - --:--"

                lesson.time = formated_time

        return schedule

    def get_schedule_day_id(self, file_id: str):
        file = self.file_controller.get_file_by_id(file_id)

        if file is None:
            return

        return self.get_schedule_day(file)

    def get_schedule_day(self, file: File):
        schedule = self.update_or_get_schedule_by_id(file)
        return schedule

    def get_schedule_by_files_list(self, files: list[File]):
        return [self.get_schedule_day(file) for file in files]
