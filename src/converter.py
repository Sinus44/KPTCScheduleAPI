import copy

from src.datatypes.group import Group
from src.datatypes.lesson import Lesson
from src.datatypes.schedule import Schedule
from src.datatypes.schedule_file import File
from src.models.file_update_model import FileUpdateModel
from src.models.schedule_update_model import ScheduleUpdateModel
from src.schemes.file_update_response import FileUpdateResponse
from src.schemes.schedule_update_response import ScheduleUpdateResponse


def convert_model_to_dto_file_update(file_update_model: FileUpdateModel) -> FileUpdateResponse:
    return FileUpdateResponse(
        id=file_update_model.id,
        update_file_id=file_update_model.update_file_id,
        update_time=file_update_model.update_time,
        update_type=file_update_model.update_type
    )


def convert_model_to_dto_schedule_update(schedule_update_model: ScheduleUpdateModel) -> ScheduleUpdateResponse:
    return ScheduleUpdateResponse(
        id=schedule_update_model.id,
        update_file_id=schedule_update_model.update_file_id,
        update_time=schedule_update_model.update_time,
        update_group=schedule_update_model.update_group
    )


def convert_lesson_to_dict(lesson: Lesson) -> dict:
    return copy.deepcopy(lesson.__dict__)


def convert_group_to_dict(group: Group) -> dict:
    lessons_dict_list: list[dict] = [convert_lesson_to_dict(lesson) for lesson in group.lessons]

    return {
        "course": group.course,
        "lessons": lessons_dict_list,
        "name": group.name,
        "school_year": group.school_year,
        "spec": group.spec,
        "sub_group": group.sub_group
    }


def convert_file_to_dict(file: File) -> dict:
    return copy.deepcopy(file.__dict__)


def convert_schedule_to_dict(schedule: Schedule) -> dict:
    groups_dict: list[dict] = [convert_group_to_dict(group) for group in schedule.groups]
    file_dict: dict = convert_file_to_dict(schedule.file)

    return {
        "file": file_dict,
        "groups": groups_dict
    }


def convert_list_schedule_to_dict(schedule_list: list[Schedule]) -> list[dict]:
    return [convert_schedule_to_dict(schedule) for schedule in schedule_list]
