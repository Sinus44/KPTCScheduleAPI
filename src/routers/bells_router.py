from fastapi import APIRouter

from src.http_exceptions import InvalidParameterException
from src.schemes.bell_response import BellResponse
from src.schemes.exception_response import ExceptionResponse
from src.schemes.list_bell_blocks_response import ListBellBlocksResponse
from src.services.bell_service import BellService
from src.validator import validate_weekday_index

bells_controller = BellService()
bells_router = APIRouter(prefix="/bell", tags=["bell"])


@bells_router.get("/getAll", summary="Получить всё расписание звонков")
def bell_get_all() -> ListBellBlocksResponse:
    return bells_controller.get_all_bells().to_scheme()


@bells_router.get("/getAllLessons", summary="Получить всё расписание звонков, но только пар")
def bell_get_all_lessons() -> ListBellBlocksResponse:
    return bells_controller.get_all_lesson_bells().to_scheme()


@bells_router.get("/getByWeekdayIndex", summary="Получить звонки по индексу дня", responses={
    400: {"model": ExceptionResponse, "description": "Invalid day_index"}
})
def bell_get_by_weekday_index(weekday_index: int) -> list[BellResponse]:
    day = validate_weekday_index(weekday_index)

    if day is None:
        raise InvalidParameterException("weekday_index")

    return [bell.to_scheme() for bell in bells_controller.get_day_bells(day)]
