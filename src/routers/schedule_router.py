from fastapi import APIRouter

from src.datatypes.schedule import Schedule
from src.http_exceptions import InvalidParameterException, FileNotFoundException, ScheduleNotFoundException
from src.routers.bells_router import bells_controller
from src.routers.file_router import file_controller
from src.schemes.exception_response import ExceptionResponse
from src.schemes.schedule_response import ScheduleResponse
from src.schemes.schedules_response import SchedulesResponse
from src.services.schedule_service import ScheduleService, filter_group_by_schedule_list, filter_group_in_schedule
from src.validator import validate_date, validate_file_id, validate_group_name

schedule_controller = ScheduleService(file_controller, bells_controller)
schedule_router = APIRouter(prefix="/schedule", tags=["schedule"])


@schedule_router.get("/getAll", summary="Получить всё расписание", responses={
    422: {"model": ExceptionResponse, "description": "Invalid group_name"}
})
def schedule_get_all(group_name: str = None) -> SchedulesResponse:
    files = file_controller.get_available_files()
    schedule_list: list[Schedule] = schedule_controller.get_schedule_by_files_list(files)

    if group_name is not None:
        group_name = validate_group_name(group_name)

        if group_name is None:
            raise InvalidParameterException("group_name")

        schedule_list = filter_group_by_schedule_list(schedule_list, group_name)

    return SchedulesResponse(schedule=[schedule.to_scheme() for schedule in schedule_list])


@schedule_router.get("/getActual", summary="Получить только актуальное расписание", responses={
    422: {"model": ExceptionResponse, "description": "Invalid group_name"}
})
def schedule_get_actual(group_name: str = None) -> SchedulesResponse:
    files = file_controller.get_actual_files()
    schedule_list = schedule_controller.get_schedule_by_files_list(files)

    if group_name is not None:
        group_name = validate_group_name(group_name)

        if group_name is None:
            raise InvalidParameterException("group_name")

        schedule_list = filter_group_by_schedule_list(schedule_list, group_name)

    return SchedulesResponse(schedule=[schedule.to_scheme() for schedule in schedule_list])


@schedule_router.get("/getByFileId", summary="Получить расписание по id файла", responses={
    422: {"model": ExceptionResponse, "description": "Invalid file_id"},
    404: {"model": ExceptionResponse, "description": "File not found"}
})
def schedule_get_by_file_id(file_id: str, group_name: str = None) -> ScheduleResponse:
    file_id = validate_file_id(file_id)

    if file_id is None:
        raise InvalidParameterException("file_id")

    schedule = schedule_controller.get_schedule_day_id(file_id)

    if schedule is None:
        raise FileNotFoundException

    if group_name is not None:
        group_name = validate_group_name(group_name)

        if group_name is None:
            raise InvalidParameterException("group_name")

        schedule = filter_group_in_schedule(schedule, group_name)

    return schedule.to_scheme()


@schedule_router.get("/getByDate", summary="Получить расписание по дате", responses={
    422: {"model": ExceptionResponse, "description": "Invalid date"},
    404: {"model": ExceptionResponse, "description": "File not found"},
})
def schedule_get_by_date(date: str, group_name: str = None) -> ScheduleResponse:
    date = validate_date(date)

    if date is None:
        raise InvalidParameterException("date")

    file = file_controller.get_file_by_date(date)

    if file is None:
        raise FileNotFoundException()

    schedule = schedule_controller.get_schedule_day_id(file.id)

    if schedule is None:
        raise ScheduleNotFoundException()

    if group_name is not None:
        group_name = validate_group_name(group_name)

        if group_name is None:
            raise InvalidParameterException("group_name")

        schedule = filter_group_in_schedule(schedule, group_name)

    return schedule.to_scheme()

# @schedule_router.get("/getByDates", summary="Получить расписание по списку дат")
# def schedule_get_by_dates(dates: str):
#     dates = validate_dates(dates)
#
#     if dates is None:
#         return InvalidParameterException("dates")
#
#     files = []
#     for date in dates:
#         file = file_controller.get_file_by_date(date)
#
#         if file is None:
#             raise FileWithDateNotFoundException(date)
#
#         files.append(file)
#
#     schedules = []
#     for file in files:
#         schedule = schedule_controller.get_schedule_day(file)
#
#         if schedule is None:
#             raise InternalFileNotFoundException(file.id)
#
#         schedules.append(schedule)
#
#     return SchedulesResponse(schedule=[schedule.serialize() for schedule in schedules])


# @schedule_router.get("/getByIds", summary="Получить расписание по списку ID файлов")
# def schedule_get_by_file_ids(file_ids: str) -> SchedulesResponse:
#     file_ids = validate_file_ids(file_ids)
#
#     if file_ids is None:
#         raise InvalidParameterException("file_ids")
#
#     files = []
#     for file_id in file_ids:
#         file = file_controller.get_file_by_id(file_id)
#
#         if file is None:
#             raise FileNotFoundException()
#
#         files.append(file)
#
#     schedules = []
#     for file in files:
#         schedule = schedule_controller.get_schedule_day(file)
#
#         if schedule is None:
#             raise InternalFileNotFoundException(file.id)
#
#         schedules.append(schedule)
#
#     return SchedulesResponse(schedule=[schedule.serialize() for schedule in schedules])
#
